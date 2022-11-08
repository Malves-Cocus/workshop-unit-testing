from json import dumps

from mock import call, patch

import api


class TestMain:

    @patch.object(api.CityBikes, "networks", return_value={
        "success": True,
        "data": {
            "networks": [
                {
                    "id": "hello-world",
                    "location": {
                        "country": "DK"
                    }
                },
                {
                    "id": "foo-bar",
                    "location": {
                        "country": "UK"
                    }
                },
                {
                    "id": "the-best-country",
                    "location": {
                        "country": "BR"
                    }
                }
            ]
        }
    })
    @patch.object(api.CityBikes, "network", side_effect=[
        {
            "success": True,
            "data": {
                "network": {
                    "id": "hello-world",
                    "location": {
                        "city": "Copenhagen",
                        "country": "DK"
                    }
                }
            }
        },
        {
            "success": True,
            "data": {
                "network": {
                    "id": "foo-bar",
                    "location": {
                        "city": "London",
                        "country": "UK"
                    }
                }
            }
        }
    ])
    @patch("boto3.client")
    def test_only_expected_countries_files_are_uploaded(self,
                                                        boto3_client,
                                                        network_patch,
                                                        networks_patch):
        from main import main

        main()

        # Assert the "networks" API is called once
        assert networks_patch.call_count == 1

        # Assert the "network" API receives the correct arguments
        network_patch.assert_has_calls([
            call(by_id="hello-world"),
            call(by_id="foo-bar")
        ])

        # Assert the S3 API is called uploading the correct content
        s3 = boto3_client.return_value
        s3.put_object.assert_has_calls([
            call(Bucket="s3-workshop-unit-testing",
                 Key="DK/Copenhagen/hello-world.JSON",
                 Body=dumps({
                     "id": "hello-world",
                     "location": {
                         "city": "Copenhagen",
                         "country": "DK"
                     }
                 })),
            call(Bucket="s3-workshop-unit-testing",
                 Key="UK/London/foo-bar.JSON",
                 Body=dumps({
                     "id": "foo-bar",
                     "location": {
                         "city": "London",
                         "country": "UK"
                     }
                 }))
        ])
