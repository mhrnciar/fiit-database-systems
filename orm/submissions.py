from django.http import JsonResponse
from django.db.models import *
from orm.models import *
import datetime
import pytz
import json
from dateutil import parser


def get(request):
    params = request.GET
    if len(params) == 0:
        path = request.path.split('/')
        num = path[len(path) - 1]
        try:
            num = int(num)
            result = OrPodanieIssues.objects.get(id=num)
            response = {'response': {'id': result.id, 'br_court_name': result.br_court_name,
                                     'kind_name': result.kind_name, 'cin': result.cin,
                                     'registration_date': result.registration_date,
                                     'corporate_body_name': result.corporate_body_name, 'br_section': result.br_section,
                                     'br_insertion': result.br_insertion, 'text': result.text, 'street': result.street,
                                     'postal_code': result.postal_code, 'city': result.city}}
            return JsonResponse(response)

        except OrPodanieIssues.DoesNotExist:
            return JsonResponse({'error': {'message': 'Zaznam so zadanym ID neexistuje'}}, status=404)
        except ValueError:
            pass

    try:
        page = int(params.get('page', 1))
    except ValueError:
        page = 1
    if page < 1:
        page = 1

    try:
        per_page = int(params.get('per_page', 10))
    except ValueError:
        per_page = 10
    if per_page < 1:
        per_page = 10

    order_type = params.get('order_type', 'asc').lower()
    if order_type == 'desc':
        order_type = '-'
    else:
        order_type = ''

    order_params = params.get('order_by', '?').replace(' ', '').lower().split(',')
    order_list = []

    for column in order_params:
        if column in ('id', 'br_court_name', 'kind_name', 'cin', 'registration_date', 'corporate_body_name',
                      'br_section', 'br_insertion', 'text', 'street', 'postal_code', 'city'):
            order_list.append(order_type + column)

    gte = ''
    lte = ''
    if 'registration_date_gte' in params:
        try:
            dt = parser.parse(params['registration_date_gte'])
            gte = datetime.date(year=dt.year, month=dt.month, day=dt.day)
        except ValueError:
            gte = ''

    if 'registration_date_lte' in params:
        try:
            dt = parser.parse(params['registration_date_lte'])
            lte = datetime.date(year=dt.year, month=dt.month, day=dt.day)
        except ValueError:
            lte = ''

    if 'query' in params:
        try:
            cin = int(params['query'])
            if lte != '' and gte != '':
                total = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                       registration_date__lte=lte,
                                                       registration_date__gte=gte).count()
                result = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                        registration_date__lte=lte,
                                                        registration_date__gte=gte)
            elif lte == '' and gte != '':
                total = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                       registration_date__gte=gte).count()
                result = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                        registration_date__gte=gte)
            elif lte != '' and gte == '':
                total = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                       registration_date__lte=lte).count()
                result = OrPodanieIssues.objects.filter(Q(cin__exact=cin),
                                                        registration_date__lte=lte)
            else:
                total = OrPodanieIssues.objects.filter(Q(cin__exact=cin)).count()
                result = OrPodanieIssues.objects.filter(Q(cin__exact=cin))

        except ValueError:
            if lte != '' and gte != '':
                total = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                       Q(city__contains=params['query']),
                                                       registration_date__lte=lte,
                                                       registration_date__gte=gte).count()
                result = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                        Q(city__contains=params['query']),
                                                        registration_date__lte=lte,
                                                        registration_date__gte=gte)
            elif lte == '' and gte != '':
                total = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                       Q(city__contains=params['query']),
                                                       registration_date__gte=gte).count()
                result = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                        Q(city__contains=params['query']),
                                                        registration_date__gte=gte)
            elif lte != '' and gte == '':
                total = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                       Q(city__contains=params['query']),
                                                       registration_date__lte=lte).count()
                result = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                        Q(city__contains=params['query']),
                                                        registration_date__lte=lte)
            else:
                total = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                       Q(city__contains=params['query'])).count()
                result = OrPodanieIssues.objects.filter(Q(corporate_body_name__contains=params['query']) |
                                                        Q(city__contains=params['query']))
    else:
        if lte != '' and gte != '':
            total = OrPodanieIssues.objects.filter(registration_date__lte=lte, registration_date__gte=gte).count()
            result = OrPodanieIssues.objects.filter(registration_date__lte=lte, registration_date__gte=gte)
        elif lte == '' and gte != '':
            total = OrPodanieIssues.objects.filter(registration_date__gte=gte).count()
            result = OrPodanieIssues.objects.filter(registration_date__gte=gte)
        elif lte != '' and gte == '':
            total = OrPodanieIssues.objects.filter(registration_date__lte=lte).count()
            result = OrPodanieIssues.objects.filter(registration_date__lte=lte)
        else:
            total = OrPodanieIssues.objects.all().count()
            result = OrPodanieIssues.objects.all()

    page_num = (page - 1) * per_page

    if len(order_list) > 1 and order_type == '-':
        first = order_list[0].replace('-', '')
        order_list.pop(0)
        result = result.order_by(F(first).desc(nulls_last=True), *order_list)[page_num:(page_num + per_page)]
    elif len(order_list) == 1 and order_type == '-':
        result = result.order_by(F(order_list[0]).desc(nulls_last=True))[page_num:(page_num + per_page)]
    elif order_type == '':
        result = result.order_by(*order_list)[page_num:(page_num + per_page)]

    response = {'items': []}
    pages_count = total // per_page
    if total % per_page != 0:
        pages_count += 1

    response['metadata'] = {'page': page, 'per_page': per_page, 'pages': pages_count, 'total': total}

    for row in result:
        entry = {'id': row.id, 'br_court_name': row.br_court_name, 'kind_name': row.kind_name, 'cin': row.cin,
                 'registration_date': row.registration_date, 'corporate_body_name': row.corporate_body_name,
                 'br_section': row.br_section, 'br_insertion': row.br_insertion, 'text': row.text, 'street': row.street,
                 'postal_code': row.postal_code, 'city': row.city}
        response['items'].append(entry)

    return JsonResponse(response)


def post(request):
    body_unicode = request.body.decode('utf-8')
    params = json.loads(body_unicode)
    errorstr = {'errors': []}
    cin = 0
    date = datetime.date.today()
    year = date.year

    if 'br_court_name' not in params:
        errorstr['errors'].append({'field': 'br_court_name', 'reasons': ['required']})

    if 'kind_name' not in params:
        errorstr['errors'].append({'field': 'kind_name', 'reasons': ['required']})

    if 'cin' not in params:
        errorstr['errors'].append({'field': 'cin', 'reasons': ['required']})
    else:
        try:
            cin = int(params['cin'])
        except ValueError:
            errorstr['errors'].append({'field': 'cin', 'reasons': ['required', 'not_number']})

    if 'registration_date' not in params:
        errorstr['errors'].append({'field': 'registration_date', 'reasons': ['required']})
    else:
        try:
            dt = parser.parse(params['registration_date']).astimezone(pytz.utc)
            date = datetime.date(dt.year, dt.month, dt.day)
            if date.year != year:
                errorstr['errors'].append({'field': 'registration_date', 'reasons': ['required', 'invalid_range']})
        except ValueError:
            errorstr['errors'].append({'field': 'registration_date', 'reasons': ['required', 'invalid_date']})

    if 'corporate_body_name' not in params:
        errorstr['errors'].append({'field': 'corporate_body_name', 'reasons': ['required']})

    if 'br_section' not in params:
        errorstr['errors'].append({'field': 'br_section', 'reasons': ['required']})

    if 'br_insertion' not in params:
        errorstr['errors'].append({'field': 'br_insertion', 'reasons': ['required']})

    if 'text' not in params:
        errorstr['errors'].append({'field': 'text', 'reasons': ['required']})

    if 'street' not in params:
        errorstr['errors'].append({'field': 'street', 'reasons': ['required']})

    if 'postal_code' not in params:
        errorstr['errors'].append({'field': 'postal_code', 'reasons': ['required']})
    else:
        try:
            int(params['postal_code'])
        except ValueError:
            errorstr['errors'].append({'field': 'postal_code', 'reasons': ['required', 'not_number']})

    if 'city' not in params:
        errorstr['errors'].append({'field': 'city', 'reasons': ['required']})

    if len(errorstr['errors']) != 0:
        return JsonResponse(errorstr, status=422)

    # Pre created_at, updated_at a published_at sa zisti momentalny cas prekonvertovany na UTC. Published_at v databaze
    # ma datum o den pred datumom created_at a update_at s vynulovanym casom, takze published_at sa este upravi na dany
    # tvar. Nakoniec sa este posklada adresa zo street, postal_code a city.
    now = datetime.datetime.now().astimezone(pytz.timezone('UTC'))
    published_at = datetime.datetime(now.year, now.month, now.day - 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
    address = params['street'] + ', ' + params['postal_code'] + ' ' + params['city']

    bulletin_count = BulletinIssues.objects.filter(year=now.year).order_by('-number')[0]
    bulletin_obj = BulletinIssues(year=now.year, number=(bulletin_count.number+1),
                                  published_at=published_at, created_at=now, updated_at=now)
    bulletin_obj.save()
    bulletin_id = bulletin_obj.id

    raw_obj = RawIssues(bulletin_issue_id=bulletin_id, file_name='-', content='-', created_at=now, updated_at=now)
    raw_obj.save()
    raw_id = raw_obj.id

    or_podanie_obj = OrPodanieIssues(bulletin_issue_id=bulletin_id, raw_issue_id=raw_id, br_mark='-', br_court_code='-',
                                     br_court_name=params['br_court_name'], kind_code='-', kind_name=params['kind_name'],
                                     cin=cin, registration_date=date, corporate_body_name=params['corporate_body_name'],
                                     br_section=params['br_section'], br_insertion=params['br_insertion'],
                                     text=params['text'], created_at=now, updated_at=now, address_line=address,
                                     street=params['street'], postal_code=params['postal_code'], city=params['city'])
    or_podanie_obj.save()
    or_podanie_id = or_podanie_obj.id

    result = OrPodanieIssues.objects.get(id=or_podanie_id)
    response = {'response': {'id': result.id, 'br_court_name': result.br_court_name, 'kind_name': result.kind_name,
                             'cin': result.cin, 'registration_date': result.registration_date,
                             'corporate_body_name': result.corporate_body_name, 'br_section': result.br_section,
                             'br_insertion': result.br_insertion, 'text': result.text, 'street': result.street,
                             'postal_code': result.postal_code, 'city': result.city}}

    return JsonResponse(response, status=201)


def put(request):
    path = request.path.split('/')
    num = path[len(path) - 1]
    try:
        num = int(num)
    except ValueError:
        num = None

    if num is None:
        return JsonResponse({'error': {'message': 'Nebolo zadane ID'}}, status=422)

    try:
        obj = OrPodanieIssues.objects.get(id=num)
    except OrPodanieIssues.DoesNotExist:
        return JsonResponse({'error': {'message': 'Zaznam so zadanym ID neexistuje'}}, status=404)

    body_unicode = request.body.decode('utf-8')
    params = json.loads(body_unicode)
    if len(params) == 0:
        return JsonResponse({'error': {'message': 'Neboli zadane ziadne parametre'}}, status=422)

    errorstr = {'errors': []}

    if 'br_court_name' in params:
        obj.br_court_name = params['br_court_name']

    if 'kind_name' in params:
        obj.kind_name = params['kind_name']

    if 'cin' in params:
        try:
            cin = int(params['cin'])
            obj.cin = cin
        except ValueError:
            errorstr['errors'].append({'field': 'cin', 'reasons': 'not_number'})

    if 'registration_date' in params:
        try:
            dt = parser.parse(params['registration_date']).astimezone(pytz.utc)
            date = datetime.date(dt.year, dt.month, dt.day)
            obj.registration_date = date
            if date > datetime.datetime.today():
                errorstr['errors'].append({'field': 'registration_date', 'reasons': 'invalid_range'})
        except ValueError:
            errorstr['errors'].append({'field': 'registration_date', 'reasons': 'not_date'})

    if 'corporate_body_name' in params:
        obj.corporate_body_name = params['corporate_body_name']

    if 'br_section' in params:
        obj.br_section = params['br_section']

    if 'br_insertion' in params:
        obj.br_insertion = params['br_insertion']

    if 'text' in params:
        obj.text = params['text']

    if 'street' in params:
        try:
            int(params['street'])
            errorstr['errors'].append({'field': 'street', 'reasons': 'not_string'})
        except ValueError:
            obj.street = params['street']

    if 'postal_code' in params:
        try:
            int(params['postal_code'])
            obj.postal_code = params['postal_code']
        except ValueError:
            errorstr['errors'].append({'field': 'postal_code', 'reasons': 'not_number'})

    if 'city' in params:
        try:
            int(params['city'])
            errorstr['errors'].append({'field': 'city', 'reasons': 'not_string'})
        except ValueError:
            obj.street = params['city']

    address = obj.street + ', ' + obj.postal_code + ' ' + obj.city
    obj.address_line = address

    now = datetime.datetime.now()
    obj.updated_at = now

    if len(errorstr['errors']) != 0:
        return JsonResponse(errorstr, status=422)

    obj.save()
    or_podanie_id = obj.id

    result = OrPodanieIssues.objects.get(id=or_podanie_id)
    response = {'response': {'id': result.id, 'br_court_name': result.br_court_name, 'kind_name': result.kind_name,
                             'cin': result.cin, 'registration_date': result.registration_date,
                             'corporate_body_name': result.corporate_body_name, 'br_section': result.br_section,
                             'br_insertion': result.br_insertion, 'text': result.text, 'street': result.street,
                             'postal_code': result.postal_code, 'city': result.city}}

    return JsonResponse(response, status=201)


def delete(request):
    path = request.path.split('/')
    num = path[len(path) - 1]
    try:
        num = int(num)
    except ValueError:
        num = None

    if num is not None:
        if OrPodanieIssues.objects.filter(id=num).exists():
            id_query = OrPodanieIssues.objects.get(id=num)
            bulletin_id = id_query.bulletin_issue_id
            raw_id = id_query.raw_issue_id

            bulletin_count = OrPodanieIssues.objects.filter(bulletin_issue_id=bulletin_id).count()
            raw_count = OrPodanieIssues.objects.filter(raw_issue_id=raw_id).count()

            OrPodanieIssues.objects.filter(id=num).delete()

            if bulletin_count == 1:
                BulletinIssues.objects.filter(id=bulletin_id).delete()
            if raw_count == 1:
                RawIssues.objects.filter(id=raw_id).delete()

            return JsonResponse({}, status=204)

        else:
            return JsonResponse({'error': {'message': 'Zaznam neexistuje'}}, status=404)

    else:
        return JsonResponse({'error': {'message': 'Nebolo zadane ID'}}, status=422)
