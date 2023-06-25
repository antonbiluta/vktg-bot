import json


def comp():
    carousel = {
        "type": "carousel",
        "elements": [
            {
                "photo_id": "-198776140_457239032",
                "title": "СтудСовет",
                "description": "Студенческий совет \nФКТиПМ КубГУ",
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/fktpm_ss"
                },
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "Привет",
                            "payload": "{}"
                        },

                    },
                    {
                        "action": {
                            "type": "open_link",
                            "link": "https://vk.com/fktpm_ss",

                            "label": "Перейти в группу 🌚",
                            "payload": "{}"
                        },
                    }
                ]
            },
            {
                "photo_id": "-198776140_457239028",
                "title": "Профбюро",
                "description": "Профбюро \nФКТиПМ КубГУ",
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/prof_fpm"
                },
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "Привет",
                            "payload": "{}"
                        },

                    },
                    {
                        "action": {
                            "type": "open_link",
                            "link": "https://vk.com/prof_fpm",

                            "label": "Перейти в группу 🌚",
                            "payload": "{}"
                        },
                    }
                ]
            },
            {
                "photo_id": "-198776140_457239030",
                "title": "СНО ФКТиПМ",
                "description": "Студенческое научное общество ФКТиПМ КубГУ",
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/sno_fktipm"
                },
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "Привет",
                            "payload": "{}"
                        },

                    },
                    {
                        "action": {
                            "type": "open_link",
                            "link": "https://vk.com/sno_fktipm",

                            "label": "Перейти в группу 🌚",
                            "payload": "{}"
                        },
                    }
                ]
            },
            {
                "photo_id": "-198776140_457239029",
                "title": "ОСО КубГУ",
                "description": "Объединенный Совет Обучающихся КубГУ (ОСО)",
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/oso_kubsu"
                },
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "Привет",
                            "payload": "{}"
                        },

                    },
                    {
                        "action": {
                            "type": "open_link",
                            "link": "https://vk.com/oso_kubsu",

                            "label": "Перейти в группу 🌚",
                            "payload": "{}"
                        },
                    }
                ]
            }
        ]
    }

    carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel