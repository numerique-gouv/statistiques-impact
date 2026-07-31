import uuid
import sys


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.template.defaultfilters import slugify
from rest_framework_api_key.models import AbstractAPIKey
from core.utils.utils import get_last_month_limits
from django.core import exceptions


class User(AbstractBaseUser):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        help_text=_("date and time at which a record was last updated"),
        auto_now=True,
        editable=False,
    )
    email = models.EmailField(_("email address"))
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"


class Product(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    dataset_id = models.CharField(blank=True, null=False)

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def last_records(self):
        recent_records = Indicator.objects.filter(productid=self).order_by("-date")
        if not recent_records:
            return []

        last_entry_date = recent_records[0].date
        return recent_records.filter(date=last_entry_date)

    @property
    def last_indicators_date(self):
        if len(self.last_records) != 0:
            return self.last_records[0].date

        return "N/A"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    slug = models.SlugField(null=False, blank=False)
    productid = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        db_column="productId",
        related_name="indicators",
    )
    indicateur = models.CharField(max_length=100)
    valeur = models.FloatField()
    unite_mesure = models.CharField(default="unités")
    frequence_monitoring = models.CharField(default="monthly")
    date = models.CharField()
    date_debut = models.CharField(blank=True, null=True)
    est_periode = models.BooleanField(default=True)
    est_automatise = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        help_text=_("date and time at which a record was last updated"),
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_table = "indicator"
        verbose_name = _("indicator")
        verbose_name_plural = _("indicators")
        constraints = [
            models.UniqueConstraint(
                fields=["productid", "indicateur", "frequence_monitoring"],
                name="no_duplicate_indicators",
            ),
        ]
        ordering = ("-date",)

    def save(self, *args, **kwargs):
        """Call `full_clean` and fill slug if necessary before saving."""
        self.slug = self.get_slug()
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_slug(self):
        """Compute slug value from name."""
        return slugify(self.indicateur)[:50]

    def validate(self, data):
        if data.est_periode and not data.date_debut:
            if data.frequence_monitoring == "monthly":
                data.date_debut = data.date.replace(day=1)

    def __str__(self):
        return f"{self.indicateur} on {self.productid}"


class ProductAPIKey(AbstractAPIKey):
    product = models.ForeignKey(
        "Product",
        models.DO_NOTHING,
        db_column="product",
        blank=False,
        null=False,
        related_name="api_keys",
    )

    class Meta:
        db_table = "api_keys"
        verbose_name = _("API key")
        verbose_name_plural = _("API keys")


class Adaptor(models.Model):
    """Adaptor model"""

    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        db_column="product",
        related_name="adaptor",
        blank=True,
        null=True,
    )
    indicator = models.CharField(blank=True, null=True)

    source_url = models.CharField(blank=True, null=True)
    client = models.CharField(
        verbose_name=_("client to treat data"),
        help_text=_("name of the client used to fetch and treat"),
        blank=False,
        null=False,
    )
    frequence_monitoring = models.CharField(blank=True, null=True)

    status = models.CharField()
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        db_table = "adaptor"
        verbose_name = _("Adaptor")
        verbose_name_plural = _("Adaptors")
        unique_together = (("product", "indicator"),)

    def get_client(self):
        """Get client or return error."""
        return getattr(sys.modules["core.clients"], self.client)(adaptor=self)

    def get_data(self):
        """Call client to get last available data."""
        client = self.get_client()
        return client.get_data()

    def save_last_month_indicator(self):
        """Call client to get last available data and save it."""
        start_date, end_date = get_last_month_limits()
        client = self.get_client()
        data = client.get_data()

        for entry in data:
            try:
                product = Product.objects.get(name=entry["product"])
                indicator = Indicator.objects.get(
                    indicateur=entry["indicator"], productid__name=product
                )
            except Product.DoesNotExist:
                print(f"Product {product} not found.")
            except Indicator.DoesNotExist:
                print(
                    f"Indicator '{entry['indicator']}' not found for product '{product}'."
                )

            else:
                try:
                    Record.objects.create(
                        indicator=indicator,
                        end_date=end_date,
                        start_date=start_date
                        if indicator.frequence_monitoring in ["mensuelle", "monthly"]
                        else None,
                        value=entry["value"],
                        is_auto_added=True,
                    )
                except ValueError:
                    print(
                        f"ValueError occured when trying to create indicator {entry['indicator']}"
                    )
                except exceptions.ValidationError as error:
                    print(error)


class Record(models.Model):
    """
    Single record of an indicator. Related to product through indicator.
    """

    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    indicator = models.ForeignKey(
        "Indicator",
        on_delete=models.PROTECT,
        db_column="indicator",
        related_name="records",
    )
    value = models.FloatField()
    end_date = models.DateField()
    start_date = models.DateField(blank=True, null=True)
    is_auto_added = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        help_text=_("date and time at which a record was last updated"),
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_table = "record"
        verbose_name = _("record")
        verbose_name_plural = _("records")
        # add uniqueconstraint after indicator model improvement
        ordering = ("-end_date",)
