import codecs
import datetime
import os
import re

from django.conf import settings

from extranet.models import IncomeQuality, Deliveries, Sales, SpeciesHarvest, Applied, CtaCte, TicketsAnalysis, Stock

BATCH_SIZE = 10000

def evalDate(date):
    # Catch format error in date
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def evalDateHour(date):
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y %I:%M:%S %p").strftime("%Y-%m-%d")
    except ValueError:
        return None

def evalFloat(num):
    try:
        return float(num.replace('.', '').replace(',','.'))
    except ValueError:
        return 0

def evalInt(num):
    try:
        return int(num.replace('.', '').replace(',','.'))
    except ValueError:
        return 0

def evalText(text):
    # Decode text in latin iso-8859-1 like (0xd1 --> ñ)
    # return unicode(text.strip(' ').decode('iso-8859-1'))
    return text

def evalTextUTF8(text):
    # return unicode(text.strip(' ').decode('utf-8'))
    return text


def importIncomeQuality():
    for filename in os.listdir(settings.EXTRANET_DIR):
        if 'ANALISIS' in filename:
            species = re.search(r"\[([A-Za-z0-9_]+)\]", filename)
            print(filename, species.group(1))

            txt = os.path.join(settings.EXTRANET_DIR, filename)
            try:
                with open(txt, 'r', encoding='iso-8859-1') as file:
                    if IncomeQuality.objects.exists():
                        IncomeQuality.objects.filter(species=species).delete()
                    record = []
                    # Exclude header
                    file.readline()
                    for line in file:
                        # Delete new line character
                        line = line.replace('\n', '').replace('\r', '')
                        if len(line) > 0:
                            data = re.split('\t', line)
                            # 99 es el mínimo número de columnas que debería tener el archivo, si tiene menos es porque el sistema exporto mal esa fila
                            if len(data) >= 99:                            
                                algoritmo_code, name = data[6][:7], data[6][8:]
                                field, field_description = data[7].split(' ')[0], ' '.join(data[7].split(' ')[1:])
                                plant, plant_description = data[36].split(' ')[0], ' '.join(data[36].split(' ')[1:])
                                
                                record.append(
                                    IncomeQuality(
                                        species = evalText(data[0]),
                                        harvest = evalText(data[1]),
                                        ticket = 'TK ' + evalText(data[2].strip()),
                                        income = evalText(data[3].strip()),
                                        cp = evalText(data[5].strip()),
                                        algoritmo_code = evalInt(algoritmo_code),
                                        name = evalText(name),
                                        field = evalInt(field),
                                        field_description = evalText(field_description),
                                        gross_kg = evalInt(data[9]),
                                        tare = evalInt(data[10]),
                                        net_weight = evalInt(data[11]),
                                        humidity_percentage = evalFloat(data[12]),
                                        humidity_volatile_reduction = evalFloat(data[13]),
                                        humidity_volatile_kg = evalInt(data[14]),
                                        dry_kg = evalInt(data[15]),
                                        quality_percentage = evalFloat(data[16]),
                                        conditioning_kg = evalInt(data[17]),
                                        item_1 = evalFloat(data[20]),
                                        item_2 = evalFloat(data[21]),
                                        item_3 = evalFloat(data[22]),
                                        item_4 = evalFloat(data[23]),
                                        item_5 = evalFloat(data[24]),
                                        item_6 = evalFloat(data[25]),
                                        item_7 = evalFloat(data[26]),
                                        item_8 = evalFloat(data[27]),
                                        item_9 = evalFloat(data[28]),
                                        item_10 = evalFloat(data[29]),
                                        item_11 = evalFloat(data[30]),
                                        item_12 = evalFloat(data[31]),
                                        item_13 = evalFloat(data[32]),
                                        item_14 = evalFloat(data[33]),
                                        item_15 = evalFloat(data[34]),
                                        plant = evalInt(plant),
                                        plant_description = evalText(plant_description),
                                        shaking_reduction = evalFloat(data[37]),
                                        shaking_kg = evalInt(data[38]),
                                        volatile_percentage = evalFloat(data[39]),
                                        volatile_kg = evalInt(data[40]),
                                        quality_reduction = evalInt(data[41]),
                                        grade = evalInt(data[43]),
                                        factor = evalFloat(data[44]),
                                        speciesharvest = evalText(data[0]) + evalText(data[1]),
                                        bonus_item_1 = evalFloat(data[47]), 
                                        bonus_item_2 = evalFloat(data[48]),
                                        bonus_item_3 = evalFloat(data[40]),
                                        bonus_item_4 = evalFloat(data[50]),
                                        bonus_item_5 = evalFloat(data[51]),
                                        bonus_item_6 = evalFloat(data[52]),
                                        bonus_item_7 = evalFloat(data[53]),
                                        bonus_item_8 = evalFloat(data[54]),
                                        bonus_item_9 = evalFloat(data[55]),
                                        bonus_item_10 = evalFloat(data[56]),
                                        bonus_item_11 = evalFloat(data[57]),
                                        bonus_item_12 = evalFloat(data[58]),
                                        bonus_item_13 = evalFloat(data[59]),
                                        bonus_item_14 = evalFloat(data[60]),
                                        bonus_item_15 = evalFloat(data[61]),
                                        reduction_item_1 = evalFloat(data[62]),
                                        reduction_item_2 = evalFloat(data[63]),
                                        reduction_item_3 = evalFloat(data[64]),
                                        reduction_item_4 = evalFloat(data[65]),
                                        reduction_item_5 = evalFloat(data[66]),
                                        reduction_item_6 = evalFloat(data[67]),
                                        reduction_item_7 = evalFloat(data[68]),
                                        reduction_item_8 = evalFloat(data[69]),
                                        reduction_item_9 = evalFloat(data[70]),
                                        reduction_item_10 = evalFloat(data[71]),
                                        reduction_item_11 = evalFloat(data[72]),
                                        reduction_item_12 = evalFloat(data[73]),
                                        reduction_item_13 = evalFloat(data[74]),
                                        reduction_item_14 = evalFloat(data[75]),
                                        reduction_item_15 = evalFloat(data[76]),
                                        services_kg = evalInt(data[77]),
                                        gluten = evalInt(data[79]),
                                        fumigation_charge = evalText(data[80]),
                                        quality_datetime = evalDate(data[98])
                                    )
                                )

                    IncomeQuality.objects.bulk_create(record, BATCH_SIZE)

            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))


def importTicketsAnalysis():
    txt = os.path.join(settings.EXTRANET_DIR, 'Analisis_Tickets.txt')
    try:
        with open(txt, 'r', encoding='utf-8') as file:
            if TicketsAnalysis.objects.exists():
                TicketsAnalysis.objects.all().delete()
            record = []
            # Exclude header
            file.readline()
            for line in file:
                # Delete new line character
                line = line.replace('\n', '').replace('\r', '')
                if len(line) > 0:
                    data = re.split('\t', line)
                    record.append(
                        TicketsAnalysis(
                            algoritmo_code = evalInt(data[20]),
                            ticket = 'TK ' + evalText(data[5]),
                            field = evalInt(data[6]),
                            field_description = evalText(data[8]),
                            species = evalText(data[9]),
                            harvest = evalText(data[10]),
                            speciesharvest = evalText(data[9]) + evalText(data[10]),
                            grade = evalInt(data[11]),
                            factor = evalFloat(data[12]),
                            analysis_costs = evalFloat(data[13]),
                            gluten = evalInt(data[14]),
                            analysis_item = evalInt(data[15]),
                            percentage = evalFloat(data[16]),
                            bonus = evalFloat(data[17]),
                            reduction = evalFloat(data[18]),
                            item_descripcion = evalTextUTF8(data[19])
                        )
                    )

            TicketsAnalysis.objects.bulk_create(record, BATCH_SIZE)

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))


def importApplied():
    txt = os.path.join(settings.EXTRANET_DIR, 'Aplicada.TXT')
    try:
        with open(txt, 'r', encoding='iso-8859-1') as file:
            if Applied.objects.exists():
                Applied.objects.all().delete()
            record = []
            for line in file:
                # Delete new line character
                line = line.replace('\n', '').replace('\r', '')
                if len(line) > 0:
                    data = re.split('\t', line)
                    record.append(
                        Applied(
                            algoritmo_code = evalInt(data[1]),
                            name = evalText(data[2]),
                            movement_type = evalText(data[13]),
                            voucher = evalText(data[16]),
                            voucher_date = evalDate(data[18]),
                            expiration_date = evalDate(data[20]),
                            issue_date = evalDate(data[21]),
                            concept = evalText(data[22]),
                            cta_cte = evalText(data[23]),
                            cta_cte_description = evalText(data[24]),
                            currency = evalText(data[31]),
                            amount_sign = evalFloat(data[36]),
                            exchange_rate = evalFloat(data[46]),
                        )
                    )

            Applied.objects.bulk_create(record, BATCH_SIZE)

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))


def importCtaCteP():
    txt = os.path.join(settings.EXTRANET_DIR, 'CtaCteP.TXT')
    try:
        with open(txt, 'r', encoding='iso-8859-1') as file:
            if CtaCte.objects.exists():
                CtaCte.objects.all().delete()
            record = []
            #r = 0
            for line in file:
                # Delete new line character
                line = line.replace('\n', '').replace('\r', '')
                if len(line) > 0:
                    data = re.split('\t', line)
                    #print r
                    record.append(
                        CtaCte(
                            algoritmo_code = evalInt(data[0]),
                            name = evalText(data[1]),
                            initial_balance_countable = evalFloat(data[14]),
                            balance = evalFloat(data[16]),
                            voucher = evalText(data[17]),
                            voucher_date = evalDate(data[19]),
                            concept = evalText(data[21]),
                            currency = evalText(data[22]),
                            movement_type = evalText(data[25]),
                            exchange_rate = evalFloat(data[26]),
                            date_1 = evalDate(data[29]),
                            date_2 = evalDate(data[30]),
                            amount_sign = evalFloat(data[45]),
                            cta_cte = evalText(data[55]),
                            cta_cte_name = evalText(data[56]),
                        )
                    )

            CtaCte.objects.bulk_create(record, BATCH_SIZE)

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))


def importKilos():
    txt = os.path.join(settings.EXTRANET_DIR, 'Web.TXT')
    try:
        with open(txt, 'r', encoding='iso-8859-1') as file:
            if Deliveries.objects.exists():
                Deliveries.objects.all().delete()
            if Sales.objects.exists():
                Sales.objects.all().delete()
            if Stock.objects.exists():
                Stock.objects.all().delete()
            if SpeciesHarvest.objects.exists():
                SpeciesHarvest.objects.all().delete()
            record_deliveries = []
            record_sales = []
            record_species = []

            # Create a Set to store the clients ID's for the Stock calculations
            clients = set()
            stocks = dict()

            for line in file:
                # Delete new line character
                line = line.replace('\n', '').replace('\r', '')
                if len(line) > 0:
                    data = re.split('\t', line)

                    # Build Deliveries and Sales data
                    if data[2] == '1':
                        record_deliveries.append(
                            Deliveries(
                                algoritmo_code = evalInt(data[0]),
                                name = evalText(data[1]),
                                indicator = evalText(data[2]),
                                species = evalText(data[3]),
                                harvest = evalText(data[4]),
                                speciesharvest = evalText(data[3]) + evalText(data[4]),
                                species_description = evalText(data[5]),
                                field = evalInt(data[6]),
                                field_description = evalText(data[7]),
                                date = evalDate(data[8]),
                                voucher = evalText(data[9]),
                                gross_kg = evalInt(data[10]),
                                humidity_percentage = evalFloat(data[11]),
                                humidity_reduction = evalFloat(data[12]),
                                humidity_kg = evalInt(data[13]),
                                shaking_reduction = evalFloat(data[14]),
                                shaking_kg = evalInt(data[15]),
                                volatile_reduction = evalFloat(data[16]),
                                volatile_kg = evalInt(data[17]),
                                price_per_yard = evalFloat(data[18]),
                                driver_code = evalInt(data[19]),
                                driver_name = evalText(data[20]),
                                factor = evalFloat(data[21]),
                                grade = evalInt(data[22]),
                                gluten = evalInt(data[23]),
                                number_1116A = evalInt(data[24]),
                                km = evalInt(data[25]),
                                external_voucher_number = evalInt(data[29]),
                                service_billing_number = evalInt(data[39]),
                                service_billing_date = evalDate(data[40]),
                                service_billing = evalText(data[41]),
                                to_date = evalDate(data[45]),
                                observations = evalText(data[46]),
                                follow_destination = evalText(data[47]),
                                net_weight = evalInt(data[49]),
                                tare = evalInt(data[50]),
                            )
                        )
                    else:
                        if data[9][0:2] != 'AD':
                            record_sales.append(
                                Sales(
                                    algoritmo_code = evalInt(data[0]),
                                    name = evalText(data[1]),
                                    indicator = evalText(data[2]),
                                    species = evalText(data[3]),
                                    harvest = evalText(data[4]),
                                    speciesharvest = evalText(data[3]) + evalText(data[4]),
                                    species_description = evalText(data[5]),
                                    field = evalInt(data[6]),
                                    field_description = evalText(data[7]),
                                    date = evalDate(data[8]),
                                    voucher = evalText(data[9]),
                                    gross_kg = evalInt(data[10]),
                                    humidity_percentage = evalFloat(data[11]),
                                    humidity_reduction = evalFloat(data[12]),
                                    humidity_kg = evalInt(data[13]),
                                    shaking_reduction = evalFloat(data[14]),
                                    shaking_kg = evalInt(data[15]),
                                    volatile_reduction = evalFloat(data[16]),
                                    volatile_kg = evalInt(data[17]),
                                    price_per_yard = evalFloat(data[18]),
                                    driver_code = evalInt(data[19]),
                                    driver_name = evalText(data[20]),
                                    factor = evalFloat(data[21]),
                                    grade = evalInt(data[22]),
                                    gluten = evalInt(data[23]),
                                    number_1116A = evalInt(data[24]),
                                    km = evalInt(data[25]),
                                    external_voucher_number = evalInt(data[29]),
                                    service_billing_number = evalInt(data[39]),
                                    service_billing_date = evalDate(data[40]),
                                    service_billing = evalText(data[41]),
                                    to_date = evalDate(data[45]),
                                    observations = evalText(data[46]),
                                    follow_destination = evalText(data[47]),
                                    net_weight = evalInt(data[49]),
                                    tare = evalInt(data[50]),
                                )
                            )
                    
                    # Build stocks by client
                    client = evalInt(data[0])
                    species = evalText(data[3])
                    harvest = evalText(data[4])
                    speciesharvest = evalText(data[3]) + evalText(data[4])
                    key = str(client) + '-' + speciesharvest
                    number_1116A = evalInt(data[24])
                    net_weight = evalInt(data[49])
                    clients.add(key)
                    
                    client_data = stocks.get(key)
                    if not client_data:
                        client_data = {
                            'algoritmo_code': client,
                            'name': evalText(data[1]),
                            'species': species,
                            'harvest': harvest,
                            'speciesharvest': speciesharvest,
                            'deliveries': 0,
                            'certificated': 0,
                            'uncertified': 0,
                            'withdrawals': 0,
                            'sales': 0,
                            'settled': 0,
                            'not_settled': 0,
                            'to_set': 0,
                            'balance': 0,
                            'trade_balance': 0,
                        }
                        stocks[key] = client_data
                    if data[2] == '1':
                        stocks[key]['deliveries'] += net_weight
                        if number_1116A == 0:
                            stocks[key]['uncertified'] += net_weight
                    if data[2] == '2':
                        stocks[key]['sales'] += net_weight
                        stocks[key]['settled'] += number_1116A
                    if data[2] == '2B':
                        stocks[key]['to_set'] += net_weight
                    if data[2] == '3':
                        stocks[key]['withdrawals'] += net_weight


            # Create Deliveries and Sales
            Deliveries.objects.bulk_create(record_deliveries, BATCH_SIZE)
            Sales.objects.bulk_create(record_sales, BATCH_SIZE)

            # Create Stocks
            while len(clients) > 0:
                key = clients.pop()
                client_data = stocks[key]
                Stock.objects.create(
                    algoritmo_code = client_data['algoritmo_code'],
                    name = client_data['name'],
                    species = client_data['species'],
                    harvest = client_data['harvest'],
                    speciesharvest = client_data['speciesharvest'],
                    deliveries = client_data['deliveries'],
                    certificated = client_data['deliveries'] - client_data['uncertified'],
                    uncertified = client_data['uncertified'],
                    withdrawals = client_data['withdrawals'],
                    sales = client_data['sales'],
                    settled = client_data['settled'],
                    not_settled = client_data['sales'] - client_data['settled'],
                    to_set = client_data['to_set'],
                    balance = client_data['deliveries'] - client_data['sales'] - client_data['withdrawals'],
                    trade_balance = client_data['deliveries'] - client_data['sales'] - client_data['withdrawals'] - client_data['to_set']
                )

            # Create speciesharvest table
            species_d = Deliveries.objects.values('algoritmo_code', 'species', 'harvest', 'speciesharvest', 'species_description').order_by('-harvest','species').distinct()
            for s in species_d:
                record_species.append(
                    SpeciesHarvest(
                        algoritmo_code = s['algoritmo_code'],
                        movement_type = 'D',
                        species = s['species'],
                        harvest = s['harvest'],
                        speciesharvest = s['speciesharvest'],
                        species_description = s['species_description'],
                    )
                )

            species_s = Sales.objects.values('algoritmo_code', 'species', 'harvest', 'speciesharvest', 'species_description').order_by('-harvest','species').distinct()
            for s in species_s:
                record_species.append(
                    SpeciesHarvest(
                        algoritmo_code = s['algoritmo_code'],
                        movement_type = 'S',
                        species = s['species'],
                        harvest = s['harvest'],
                        speciesharvest = s['speciesharvest'],
                        species_description = s['species_description'],
                    )
                )

            SpeciesHarvest.objects.bulk_create(record_species, BATCH_SIZE)

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
