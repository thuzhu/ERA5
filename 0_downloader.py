import cdsapi
import pandas as pd
import datetime

START_TIME = '2018/1/1'
END_TIME = datetime.datetime.today() - datetime.timedelta(days=7)
VARIABLE = '2m_temperature'


def main():
    for date in pd.date_range(START_TIME, END_TIME):
        print('[New] Getting t2m data on %s' % date.strftime('%Y%m%d'))
        get_ERA5_data(VARIABLE, date)


def get_ERA5_data(variable, date):
    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': variable,
            'year': str(date.year),
            'month': str(date.month),
            'day': str(date.day),
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'format': 'netcdf',
        },
        'Data/t2m_%s.nc' % date.strftime('%Y%m%d'))


if __name__ == '__main__':
    main()
