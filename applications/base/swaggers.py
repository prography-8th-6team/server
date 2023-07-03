from drf_yasg import openapi

error_message_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
    },
)

billing_create_api_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'paid_by': openapi.Schema(type=openapi.TYPE_INTEGER),
        'paid_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
        'currency': openapi.Schema(type=openapi.TYPE_STRING),
        'category': openapi.Schema(type=openapi.TYPE_STRING),
        'settlements': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                },
            ),
        ),
        'images': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_FILE,
            ),
        ),
    },
    required=['title', 'paid_by', 'paid_date', 'currency', 'settlements'],
)


dispatch_settlement_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user': openapi.Schema(type=openapi.TYPE_INTEGER),
        'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
    },
    required=['user', 'amount'],
)


authorizaion_parameters = openapi.Parameter(
    'Authorization', openapi.IN_HEADER,
    description="accesstoken은 필수입니다.",
    type=openapi.TYPE_STRING, required=True)

billing_get_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'result': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'balances': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'user': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'paid_by': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                                },
                            ),
                        },
                    ),
                ),
                'user_amounts': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        },
                    ),
                ),
            },
        ),
    },
)