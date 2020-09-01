import codecs
import datetime
import os
import re

from django.conf import settings

from website.models import TicketsAnalysis
from website.models import CtaCte
from website.models import Deliveries
from website.models import Sales
from website.models import Applied
from website.models import SpeciesHarvest

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

            TicketsAnalysis.objects.bulk_create(record)

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

            Applied.objects.bulk_create(record)

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

            CtaCte.objects.bulk_create(record)

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
            if SpeciesHarvest.objects.exists():
                SpeciesHarvest.objects.all().delete()
            record_deliveries = []
            record_sales = []
            record_species = []
            for line in file:
                # Delete new line character
                line = line.replace('\n', '').replace('\r', '')
                if len(line) > 0:
                    data = re.split('\t', line)
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

            Deliveries.objects.bulk_create(record_deliveries)
            Sales.objects.bulk_create(record_sales)

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

            SpeciesHarvest.objects.bulk_create(record_species[j:j+BULK_SIZE])

    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
