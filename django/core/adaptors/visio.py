from core.adaptors.posthog import PostHogAdaptor


class VisioAdaptor(PostHogAdaptor):
    """Adaptor to fetch and send Visio statistics."""

    slug = "visio"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "project_id": "32648",
            "insight_id": "1550533",
        }
    ]
