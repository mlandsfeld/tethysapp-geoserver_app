import random
import string

from django.shortcuts import render
from tethys_sdk.permissions import login_required
from django.views.decorators.csrf import csrf_exempt

from tethys_sdk.gizmos import *
from .app import GeoserverApp as app
from tethys_sdk.gizmos import MapView 

WORKSPACE = 'geoserver_app'
#GEOSERVER_URI = 'https://chc-ewx2.chc.ucsb.edu:8443/geoserver-app'
GEOSERVER_URI = 'http://www.example.com/geoserver-app'

@csrf_exempt
#@login_required()
def home(request):
    """
    Controller for the home page 
    """
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)
    #eros_geoserver_engine = app.get_spatial_dataset_service(name='EROS_geoserver', as_engine=True)
    print('In home(request) controller')


    #-----------------------------

    eo_layers = "chirps_global_1-month-07-2016_mm_data,africa:g2008_af_1"
    eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_monthly_data_raster.png'
    geoe5_time='2021-08-11'
    eo_geoserver_url = 'https://chc-ewx2.chc.ucsb.edu:8443/geoserver/wms'
   
    eo_options = [
      ("CHIRPS data", "chirps_global_1-month-{month}-{year}_mm_data,africa:g2008_af_1"), 
      ("CHIRPS anomaly", "chirps_global_1-month-{month}-{year}_mm_anomaly,africa:g2008_af_1"), 
      ("CHIRPS z-score", "chirps_global_1-month-{month}-{year}_none_z-score,africa:g2008_af_1"), 
      ("LST Data", "lst_global_1-month-{month}-{year}_C_data,africa:g2008_af_1"), 
      ("LST Anomaly", "lst_global_1-month-{month}-{year}_C_anomaly,africa:g2008_af_1"), 
      ("LST Z-score", "lst_global_1-month-{month}-{year}_none_z-score,africa:g2008_af_1"), 
      ("CHIRTSmax", "chirtsmax_global_1-month-{month}-{year}_mm_data,africa:g2008_af_1"),
      ("Hobbins RefET", "hobbinset_global_1-month-{month}-{year}_mm_data,africa:g2008_af_1"),
      ("MODIS NDVI", "fews_emodisndvic6v2_africa_dekad_data:emodisndvic6v2_africa_dekad_data,fews_shapefile_g2008_af_1:shapefile_g2008_af_1"),
    ]
    #("MODIS NDVI", "fews_emodisndvic6v2_africa_dekad_data:emodisndvic6v2_africa_dekad_data:fews_shapefile_g2008_af_1:shapefile_g2008_af_1"),

    eo_select_options = SelectInput(
        display_text='Choose Earth Observation',
        name='eo_layers',
        multiple=False,
        options=eo_options,
        attributes={"style":"width:50%;"},
        original=True
    )

    eo_years = [
      ("--", "--"), 
      ("1980", "1980"), 
      ("1981", "1981"), 
      ("1982", "1982"), 
      ("1983", "1983"), 
      ("1984", "1984"), 
      ("1985", "1985"), 
      ("1986", "1986"), 
      ("1987", "1987"), 
      ("1988", "1988"), 
      ("1989", "1989"), 
      ("1990", "1990"), 
      ("1991", "1991"), 
      ("1992", "1992"), 
      ("1993", "1993"), 
      ("1994", "1994"), 
      ("1995", "1995"), 
      ("1996", "1996"), 
      ("1997", "1997"), 
      ("1998", "1998"), 
      ("1999", "1999"), 
      ("2000", "2000"), 
      ("2001", "2001"), 
      ("2002", "2002"), 
      ("2003", "2003"), 
      ("2004", "2004"), 
      ("2005", "2005"), 
      ("2006", "2006"), 
      ("2007", "2007"), 
      ("2008", "2008"), 
      ("2009", "2009"), 
      ("2010", "2010"), 
      ("2011", "2011"), 
      ("2012", "2012"), 
      ("2013", "2013"), 
      ("2014", "2014"), 
      ("2015", "2015"), 
      ("2016", "2016"), 
      ("2017", "2017"), 
      ("2018", "2018"), 
      ("2019", "2019"), 
      ("2020", "2020"),
      ("2021", "2021"),
    ]

    eo_years_options = SelectInput(
        display_text='Choose Year',
        name='eo_years',
        multiple=False,
        options=eo_years,
        attributes={"style":"width:75%;"},
        initial='2016',
        original=True,
    )

    eo_months = [
      ("01", "01"), 
      ("02", "02"), 
      ("03", "03"), 
      ("04", "04"), 
      ("05", "05"), 
      ("06", "06"), 
      ("07", "07"), 
      ("08", "08"), 
      ("09", "09"), 
      ("10", "10"), 
      ("11", "11"), 
      ("12", "12"), 
    ]

    eo_months_options = SelectInput(
        display_text='Choose Month',
        name='eo_months',
        multiple=False,
        options=eo_months,
        initial='07',
        attributes={"style":"width:33%;"},
        original=True
    )

    eo_dekads = [
      ("01", "01"), 
      ("02", "11"), 
      ("03", "21"), 
    ]

    eo_dekads_options = SelectInput(
        display_text='Choose Dekad',
        name='eo_dekads',
        multiple=False,
        options=eo_dekads,
        initial='01',
        attributes={"style":"width:75%;"},
        original=True
    )


    #-----------------------------

    
    forecast_layer = "L_fcast_MAPE_ET"
    forecast_sld_file = "https://chc-ewx2.chc.ucsb.edu/sld/DEFAULT.SLD/NO_MATCH_FOUND"
    forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield.png'
    
    forecast_options = [
      ("Current Forecast (%)",  "ET_current_CI"),
      ("Current Forecast low (%)",  "ET_current_CI_low"),
      ("Current Forecast high (%)",  "ET_current_CI_high"),
      ("Historical Forecast (%)",  "ET_forecast_pcnt"),
      ("Historical Yield Forecast (MT)",  "ET_forecast"),
      ("Historical Yield Yield Forecast Error", "ET_forecast_err"), 
      ("Historical Yield Yield Forecast MAPE", "ET_MAPE"), 
      ("Area", "area"), 
      ("Area mean (10 years)", "area_mean_10yr"), 
      ("Area mean (all years)", "area_mean_all"), 
      ("Production", "prod"), 
      ("Production (mean 10 years)", "prod_mean_10yr"), 
      ("Production (mean all years)", "prod_mean_all"), 
      ("Yield", "yield"), 
      ("Yield (mean 10 years)", "yield_mean_10yr"), 
      ("Yield (mean all years)", "yield_mean_all"), 
    ]
    
    forecast_select_options = SelectInput(
        display_text='Choose Yield',
        name='forecast_layer',
        multiple=False,
        options=forecast_options,
        attributes={"style":"width:50%;"},
        original=True
    )


    forecast_years = [
      ("--", "--"), 
      ("1980", "1980"), 
      ("1981", "1981"), 
      ("1982", "1982"), 
      ("1983", "1983"), 
      ("1984", "1984"), 
      ("1985", "1985"), 
      ("1986", "1986"), 
      ("1987", "1987"), 
      ("1988", "1988"), 
      ("1989", "1989"), 
      ("1990", "1990"), 
      ("1991", "1991"), 
      ("1992", "1992"), 
      ("1993", "1993"), 
      ("1994", "1994"), 
      ("1995", "1995"), 
      ("1996", "1996"), 
      ("1997", "1997"), 
      ("1998", "1998"), 
      ("1999", "1999"), 
      ("2000", "2000"), 
      ("2001", "2001"), 
      ("2002", "2002"), 
      ("2003", "2003"), 
      ("2004", "2004"), 
      ("2005", "2005"), 
      ("2006", "2006"), 
      ("2007", "2007"), 
      ("2008", "2008"), 
      ("2009", "2009"), 
      ("2010", "2010"), 
      ("2011", "2011"), 
      ("2012", "2012"), 
      ("2013", "2013"), 
      ("2014", "2014"), 
      ("2015", "2015"), 
      ("2016", "2016"), 
      ("2017", "2017"), 
      ("2018", "2018"), 
      ("2019", "2019"), 
      ("2020", "2020"), 
      ("2021", "2021"), 
    ]

    forecast_years_options = SelectInput(
        display_text='Choose Year',
        name='forecast_years',
        multiple=False,
        options=forecast_years,
        attributes={"style":"width:75%;"},
        initial='2012',
        original=True
    )

    forecast_months = [
      ("--", "--"), 
      ("1", "1"), 
      ("2", "2"), 
      ("3", "3"), 
      ("4", "4"), 
      ("5", "5"), 
      ("6", "6"), 
      ("7", "7"), 
      ("8", "8"), 
      ("9", "9"), 
      ("10", "10"), 
      ("11", "11"), 
      ("12", "12"), 
    ]

    forecast_months_options = SelectInput(
        display_text='Choose Month',
        name='forecast_months',
        multiple=False,
        options=forecast_months,
        initial='6',
        attributes={"style":"width:50%;"},
        original=True
    )

    forecast_dekads = [
      ("--", "--"), 
      ("1", "1"), 
      ("2", "2"), 
      ("3", "3"), 
    ]

    forecast_dekads_options = SelectInput(
        display_text='Choose Dekad',
        name='forecast_dekads',
        multiple=False,
        options=forecast_dekads,
        initial='1',
        attributes={"style":"width:50%;"},
        original=True
    )

    forecast_season = [
      ("Long", "long"), 
      ("Short", "short"), 
    ]

    forecast_season_options = SelectInput(
        display_text='Choose Season',
        name='forecast_season',
        multiple=False,
        options=forecast_season,
        initial='1',
        attributes={"style":"width:60%;"},
        original=True
    )


    #-----------------------------

    if not "eo_map_layers" in locals():
        print("no EO map defined")
    eo_map_layers = []

    #if request.POST and 'eo_layer' in request.POST:
    if request.POST and 'update_maps' in request.POST:
        print("")
        print('In eo_layer Post request')
        
        eo_map_layers = []
        
        selected_layer = request.POST['eo_layers']
        print('EO selected_layer: ' + selected_layer)
        eo_select_options.initial=selected_layer
            
        
        year = request.POST['eo_years']
        eo_years_options.initial=year
        
        month = request.POST['eo_months']
        eo_months_options.initial=month
        
        dekad = request.POST['eo_dekads']
        print('selected_dekad: ' + dekad)
        eo_dekads_options.initial=dekad
        
        eo_geoserver_url = 'https://chc-ewx2.chc.ucsb.edu:8443/geoserver/wms'
        if 'fews_emodis' in selected_layer:
        	eo_geoserver_url = 'https://dmsdata.cr.usgs.gov/geoserver/wms'
        print('eo_geoserver_url: ', eo_geoserver_url)
        	
        if 'data' in selected_layer:
            print('Data legend')
            eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_monthly_data_raster.png'
        if 'anomaly' in selected_layer:
            print('Anomaly legend')
            eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_monthly_anom_raster.png'
        if 'z-score' in selected_layer:
            print('Z-score legend')
            eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_zscore_raster.png'
        if 'chirtsmax' in selected_layer:
            if 'data' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature.png'
            if 'anomaly' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature_anom.png'
            if 'zscore' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature_zscore.png'
        if 'lst_global' in selected_layer:
            if 'data' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature.png'
            if 'anomaly' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature_anom.png'
            if 'z-score' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/temperature_zscore.png'
        if 'hobbinset' in selected_layer:
            if 'data' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/refet0_monthly_data_raster.png'
        if 'ndvi' in selected_layer:
            if 'data' in selected_layer:
                eo_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/ndvi_data.png'
                        
        geoe5_time = f"{year}-{month}-{dekad}"
        print("Geoengine 5 time: " + geoe5_time)
        	
        eo_layers = selected_layer.format(month=month, year=year)
        print('eo_layers: ' + eo_layers)

        eo_geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'url': 'http://chg-ewxtest.chc.ucsb.edu:8080/geoserver/wms',
                'urlx': 'https://dmsdata.cr.usgs.gov/geoserver/gwc/service/wms',
                'params': {'LAYERS': eo_layers},
                'serverType': 'geoserver'
            },
            legend_title="",
            legend_extent=[-119, 36.5, -109, 42.5],
            legend_classes=[
              MVLegendImageClass(
                value='Precipitation',
                image_url=eo_legend_url,
              )
            ]
        )
        
        eo_map_layers.append(eo_geoserver_layer)

        #-----------------------------
    
        #if request.POST and 'update_maps' in request.POST:
        
        print("")
        print('In forecast_layer Post request', request.POST)
        
        selected_layer = request.POST['forecast_layer']
        forecast_layer = selected_layer[1]
        print('forecast selected_layer: ' + selected_layer)
        print('forecast_layer: ' + forecast_layer)
        forecast_select_options.initial=selected_layer
    
        year = request.POST['forecast_years']
        print('selected_year: ' + year)
        forecast_years_options.initial=year
        
        month = request.POST['forecast_months']
        print('selected_month: ' + month)
        forecast_months_options.initial=month
        
        dekad = request.POST['forecast_dekads']
        print('selected_dekad: ' + dekad)
        forecast_dekads_options.initial=dekad
        
        forecast_season = request.POST['forecast_season']
        print('selected_season: ' + forecast_season)
        forecast_season_options.initial = forecast_season
        
        sld_url = "https://chc-ewx2.chc.ucsb.edu/sld/"
        
        if forecast_season == 'long':
          season = "L"
        elif forecast_season == 'short':
          season = 'S'
          
        if selected_layer == "ET_forecast":
          forecast_sld_file = f"{sld_url}ET_fcast/{season}_ET_fcast_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield1.png' 
        if selected_layer == "ET_forecast_err":
          forecast_sld_file = f"{sld_url}ET_error/{season}_ET_err_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_error.png'
        if selected_layer == "ET_MAPE":
          forecast_sld_file = f"{sld_url}ET_MAPE/{season}_ET_MP_{month}_{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_MAPE.png'
        if selected_layer == "ET_forecast_pcnt":
          forecast_sld_file = f"{sld_url}ET_fcast_pcnt/{season}_ET_pcnt_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_ci.png'

        if selected_layer == "ET_current_CI":
          forecast_sld_file = f"{sld_url}ET_cur_CI/ET_cur_CI_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_ci.png'
        if selected_layer == "ET_current_CI_low":
          forecast_sld_file = f"{sld_url}ET_cur_CI/ET_cur_CI_lo_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_ci.png'
        if selected_layer == "ET_current_CI_high":
          forecast_sld_file = f"{sld_url}ET_cur_CI/ET_cur_CI_hi_{year}{month}{dekad}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield_ci.png'


        if selected_layer == "area":
          forecast_sld_file = f"{sld_url}area/area_{season}{year}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_area.png'
        if selected_layer == "area_mean_10yr":
          forecast_sld_file = f"{sld_url}area/{season}_area_mean_10yr.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_area.png'
        if selected_layer == "area_mean_all":
          forecast_sld_file = f"{sld_url}area/{season}_area_mean_all.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_area.png'
        if selected_layer == "prod":
          forecast_sld_file = f"{sld_url}prod/{season}_prod_{year}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_prod.png'
        if selected_layer == "prod_mean_10yr":
          forecast_sld_file = f"{sld_url}prod/{season}_prod_mean_10yr.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_prod.png'
        if selected_layer == "prod_mean_all":
          forecast_sld_file = f"{sld_url}prod/{season}_prod_mean_all.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_prod.png'
        if selected_layer == "yield":
          forecast_sld_file = f"{sld_url}yield/{season}_yield_{year}.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield1.png'
        if selected_layer == "yield_mean_10yr":
          forecast_sld_file = f"{sld_url}yield/{season}_yield_mean_10yr.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield1.png'
        if selected_layer == "yield_mean_all":
          forecast_sld_file = f"{sld_url}yield/{season}_yield_mean_all.sld"
          forecast_legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/crop_yield1.png'
    
        #forecast_sld_file = f"https://chc-ewx2.chc.ucsb.edu/sld/yield_ET_err_long_{year}{month}{dekad}.sld"
        print("SLD file: ", forecast_sld_file)
    
        legend_title = selected_layer.title()
        print("forecast_legend_url: ", forecast_legend_url)
    


    eo_view_options = MVView(
        projection='EPSG:4326',
        center=[41, 5],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    eo_map_options = MapView(
        height='100%',
        width='100%',
        layers=eo_map_layers,
        legend=True,
        view=eo_view_options
    )


    context = {
        'eo_map_options': eo_map_options,
        'eo_layers': eo_layers,
        'geoe5_time': geoe5_time,
        'eo_geoserver_url': eo_geoserver_url,
        'eo_select_options': eo_select_options,
        'eo_years_options': eo_years_options,
        'eo_months_options': eo_months_options,
        'eo_dekads_options': eo_dekads_options,
        'eo_legend_url': eo_legend_url,
        #'forecast_map_options': forecast_map_options,
        'forecast_select_options': forecast_select_options,
        'forecast_years_options': forecast_years_options,
        'forecast_months_options': forecast_months_options,
        'forecast_dekads_options': forecast_dekads_options,
        'forecast_layer': forecast_layer,
        'forecast_sld_file': forecast_sld_file,
        'forecast_legend_url': forecast_legend_url,
        'forecast_season_options': forecast_season_options,
    }

    return render(request, 'geoserver_app/home.html', context)
