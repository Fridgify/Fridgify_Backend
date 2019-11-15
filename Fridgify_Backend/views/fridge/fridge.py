from django.http import JsonResponse


def get_fridges(request):
    return JsonResponse([
        {"id": 1,
         "name": "Fridge_1",
         "description": "Description for fridge_1",
         "content": {
             "total": 20,
             "fresh": 5,
             "dueSoon": 13,
             "overDue": 2
         }
         },
        {"id": 2,
         "name": "Fridge_2",
         "description": "Description for fridge_2",
         "content": {
             "total": 20,
             "fresh": 5,
             "dueSoon": 13,
             "overDue": 2
         }
         },
        {"id": 3,
         "name": "Fridge_3",
         "description": "Description for fridge_3",
         "content": {
             "total": 20,
             "fresh": 5,
             "dueSoon": 13,
             "overDue": 2
         }
         },
        {"id": 4,
         "name": "Fridge_4",
         "description": "Description for fridge_4",
         "content": {
             "total": 20,
             "fresh": 5,
             "dueSoon": 13,
             "overDue": 2
         }
         }
    ], safe=False)
