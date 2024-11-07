import pandas
import argparse
import requests
from pandas.tseries.offsets import MonthEnd

API_URL = "https://stats.beta.numerique.gouv.fr/api"


def get_api_period_result(product, indicator, date_debut):
    """GET existing API results"""
    response = requests.get(f"{API_URL}/indicators/{product}")
    results = response.json()

    if indicator not in results:
        return None

    for measure in results[indicator]:
        # print(measure)
        if str(measure['date_debut']) == f'{date_debut}-01':
            return measure['valeur']
        if str(measure['date_debut']) == pandas.Period.to_timestamp(date_debut):
             return measure['valeur']
        
    # if the measure doesn't exist
    return None


def send_measure(product, indicateur, valeur, date_debut, date_fin=None):

    date_debut = pandas.Period.to_timestamp(date_debut).date()
    # .to_datetime(df[date_field]).dt.to_period('D')
    if not date_fin:
        # import pdb; pdb.set_trace()
        date_fin = str((pandas.Timestamp(date_debut) + pandas.offsets.MonthEnd(0)).date()) # almost there
    print(f"Adding {product}({date_debut} - {date_fin}) = {valeur}")

    body = {
        "productName": product,
        "indicatorDtos": [
            {
                "nom_service_public_numerique": product,
                "indicateur": indicateur,
                "valeur": valeur,
                "unite_mesure": "unite",
                "frequence_monitoring": "mensuelle",
                "date": str(date_fin),
                "date_debut": str(date_debut),
                "est_periode": True,
                "est_automatise": False,
            }
        ]
    }
    response = requests.post(
        f"{API_URL}/indicators/", 
        json=body)

    print(response.content.decode('utf-8'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Just an example",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filename", help="path to import file")
    args = parser.parse_args()
    config = vars(args)

    try: 
        df = pandas.read_csv(args.filename)
    except FileNotFoundError:
        print(f"File '{args.filename}'not found")
        exit()

    if "asam_osmose_membres" in args.filename:
        product = "osmose"

    elif "francetransfert_stats" in args.filename:
        product = "france transfert"
    
        # francetransfert_stats_envoi_quot_head.csv
        # df['month_year'] = df['date'].dt.to_period('M')
        

        frequency = df.groupby(['date']).size().reset_index(name='frequency')
        print(frequency)

    elif "webconf_collector" in args.filename:
        product="webconf"
        indicators = "participants"

        date_field = 'session_start'
        del df['filename']
        del df['desc_semaine']
        del df['nb_semaine']        

    df['period'] = pandas.to_datetime(df[date_field]).dt.to_period('M')
    frequency = df.groupby(['period', "uid"]).size().reset_index(name='frequency')

    MAU = frequency.groupby(['period'])['uid'].nunique()
    MAU.reset_index
    MAU.drop(MAU[MAU.index=="2024-07"].index) # dropping incomplete last count

    for date in MAU.index:
        
        existing_result = get_api_period_result(product, 'participants', date_debut=date)
        valeur = int(MAU[date])
        if not existing_result:
            send_measure(product, "participants", valeur, date)
        else:
            print(f"{date} - Exising result {existing_result} == {valeur} ?", existing_result== valeur)

    