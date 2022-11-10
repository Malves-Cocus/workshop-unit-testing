from json import dumps

import boto3

import api

COUNTRIES = ("DK", "UK")

s3 = boto3.client("s3", endpoint_url="http://localhost:4566")


def main():
    city_bikes_api = api.CityBikes()
    r_networks = city_bikes_api.networks()
    if not r_networks["success"]:
        print("main: api returned an error", dumps(r_networks))
        exit(1)

    for network in r_networks["data"]["networks"]:
        country = network["location"]["country"]
        if country not in COUNTRIES:
            continue

        print("main: network found", dumps(network))
        r_network = city_bikes_api.network(by_id=network["id"])
        if r_network["success"]:
            bike_detail = r_network["data"]["network"]
            key = F"{bike_detail['location']['country']}/{bike_detail['location']['city']}/{bike_detail['id']}.JSON"

            print("main: uploading file", key)
            s3.put_object(Bucket="s3-workshop-unit-testing", Key=key, Body=dumps(bike_detail))
        else:
            print("main: api returned an error", dumps(r_network))


if __name__ == "__main__":  # pragma: no cover
    main()
