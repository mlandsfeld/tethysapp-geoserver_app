import random
import string

from django.shortcuts import render
from tethys_sdk.permissions import login_required
from django.views.decorators.csrf import csrf_exempt

from tethys_sdk.gizmos import *
from .app import GeoserverApp as app


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
    print('In home(request) controller')


	#-----------------------------
    forecast_options = [
      ("ET Yield Forecast (long rains)",  "ET_forecast_long"),
      ("ET Yield Forecast Error (long rains)", "ET_forecast_err_long"), 
      ("ET Yield Forecast MAPE (long rains)", "ET_MAPE_long"), 
      ("Area (long rains)", "area_long"), 
      ("Area mean (10 years)", "area_long_mean_10yr"), 
      ("Area mean (all years)", "area_long_mean_all"), 
      ("Production (long rains)", "Area_long"), 
      ("Production (mean 10 years)", "Area_long"), 
      ("Production (mean all years)", "Area_long"), 
      ("Yield (long rains)", "Area_long"), 
      ("Yield (mean 10 years)", "Area_long"), 
      ("Yield (mean all years)", "Area_long"), 

    ]
    
    forecast_layer = "geoserver_app:ET_forecast_long"
    forecast_sld_file = ""
    
    #for l in layers:
    #    forecast_options.append((l, l))

    forecast_select_options = SelectInput(
        display_text='Choose Yield',
        name='forecast_layer',
        multiple=False,
        options=forecast_options,
        attributes={"style":"width:50%;"},
        original=True
    )

	#-----------------------------

    eo_layers = "chirps_global_1-month-07-2012_mm_anomaly,africa:g2008_af_1"
	
    eo_options = [
      ("CHIRPS data", "chirps_global_1-month-{month}-{year}_mm_data,africa:g2008_af_1"), 
      ("CHIRPS EROS data", "fews_chirps_global_month_data:chirps_global_month_data&TIME=2021-02-01"),
      ("CHIRPS anomaly", "chirps_global_1-month-{month}-{year}_mm_anomaly,africa:g2008_af_1"), 
      ("CHIRPS z-score", "chirps_global_1-month-{month}-{year}_none_z-score,africa:g2008_af_1"), 
      ("LST Data", "lst_global_1-month-{month}-{year}_C_data,africa:g2008_af_1"), 
      ("LST Anomaly", "lst_global_1-month-{month}-{year}_C_anomaly,africa:g2008_af_1"), 
      ("LST Z-score", "lst_global_1-month-{month}-{year}_none_z-score,africa:g2008_af_1"), 
      ("CHIRTmax", "chirtmax_global_1-month-{month}-{year}_C_data,africa:g2008_af_1"),
    ]


    eo_select_options = SelectInput(
        display_text='Choose Earth Observation',
        name='eo_layer',
        multiple=False,
        options=eo_options,
        attributes={"style":"width:50%;"},
        original=True
    )

	#-----------------------------

    eo_years = [
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
    ]

    eo_years_options = SelectInput(
        display_text='Choose Year',
        name='eo_years',
        multiple=False,
        options=eo_years,
        attributes={"style":"width:75%;"},
        initial='2015',
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
      ("02", "02"), 
      ("03", "03"), 
    ]

    eo_dekads_options = SelectInput(
        display_text='Choose Dekad',
        name='eo_dekads',
        multiple=False,
        options=eo_dekads,
        initial='03',
        attributes={"style":"width:75%;"},
        original=True
    )


	#-----------------------------

    forecast_years = [
      ("--", "--"), 
      ("2010", "2010"), 
      ("2011", "2011"), 
      ("2012", "2012"), 
      ("2013", "2013"), 
      ("2014", "2014"), 
      ("2015", "2015"), 
      ("2016", "2016"), 
      ("2017", "2017"), 
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


	#-----------------------------

    eo_map_layers = []

    if request.POST and 'eo_layer' in request.POST:
        print('In eo_layer Post request')
        
        selected_layer = request.POST['eo_layer']
        print('selected_layer: ' + selected_layer)
        eo_select_options.initial=selected_layer
        	
        
        year = request.POST['eo_years']
        #print('selected_year: ' + year)
        eo_years_options.initial=year
        
        month = request.POST['eo_months']
        #print('selected_month: ' + month)
        eo_months_options.initial=month
        
        if 'data' in selected_layer:
        	print('Data')
        	legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_monthly_data_raster.png'
        if 'anomaly' in selected_layer:
        	print('Anomaly')
        	legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_monthly_anom_raster.png'
        if 'z-score' in selected_layer:
        	print('Z-score')
        	legend_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_zscore_raster.png'
        	
        if 'chirps' in selected_layer:
        	legend_title = f"CHIRPS {year} {month}"
        if 'lst' in selected_layer:
        	legend_title = f"LST {year} {month}"
        	

        eo_layers = selected_layer.format(month=month, year=year)
        #layer = f"chirps_africa_1-month-{month}-{year}_mm_data,africa:g2008_af_1"
        print('eo_layers: ' + eo_layers)

        #print(type(selected_layer))
        
        eo_geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'url': 'http://chg-ewxtest.chc.ucsb.edu:8080/geoserver/wms',
                'urlx': 'https://dmsdata.cr.usgs.gov/geoserver/gwc/service/wms',
                'params': {'LAYERS': eo_layers},
                'serverType': 'geoserver'
            },
            legend_title=legend_title,
            legend_extent=[-119, 36.5, -109, 42.5],
            legend_classes=[
              MVLegendImageClass(
                value='Precipitation',
                image_url=legend_url,
              )
            ]
        )
    
        eo_map_layers.append(eo_geoserver_layer)

    
    forecast_map_layers = []

    if request.POST and 'forecast_layer' in request.POST:
        print('In forecast_layer Post request', request.POST)
        
        selected_layer = request.POST['forecast_layer']
        forecast_layer = selected_layer[1]
        print('selected_layer: ' + selected_layer)
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
        
        sld_url = "https://chc-ewx2.chc.ucsb.edu/sld/"
        
        if selected_layer == "ET_forecast_long":
          forecast_sld_file = f"{sld_url}yield_ET_long/yield_ET_long_{year}{month}{dekad}.sld"
        if selected_layer == "ET_forecast_err_long":
          forecast_sld_file = f"{sld_url}yield_ET_err_long/yield_ET_err_long_{year}{month}{dekad}.sld"
        if selected_layer == "ET_MAPE_long":
          forecast_sld_file = f"{sld_url}ET_MAPE_long/ET_MAPE_long_L_{month}_{dekad}.sld"
        if selected_layer == "area_long":
          forecast_sld_file = f"{sld_url}area/area_L{year}.sld"
        if selected_layer == "area_long_mean_10yr":
          forecast_sld_file = f"{sld_url}area/area_long_mean_10yr.sld"
        if selected_layer == "area_long_mean_all":
          forecast_sld_file = f"{sld_url}area/area_long_mean_all.sld"

        #forecast_sld_file = f"https://chc-ewx2.chc.ucsb.edu/sld/yield_ET_err_long_{year}{month}{dekad}.sld"
        print("SLD file: ", forecast_sld_file)

        legend_title = selected_layer.title()
        print("legend_title: ", legend_title)

        forecast_geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'url': 'https://chc-ewx2.chc.ucsb.edu:8443/geoserver/wms',
                'params': {'CHIRPS': selected_layer},
                'serverType': 'geoserver'
            },
            legend_title='Legend',
            legend_extent=[-119, 36.5, -109, 42.5],
            legend_classes=[
              MVLegendImageClass(
                value='Precipitation',
                image_url='https://chc-ewx2.chc.ucsb.edu/images/legends/precip_dekad_data_raster.png',
              )
            ]
        )

        forecast_map_layers.append(forecast_geoserver_layer)

    eo_view_options = MVView(
        projection='EPSG:4326',
        center=[41, 5],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    forecast_view_options = MVView(
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

    forecast_map_options = MapView(
        height='100%',
        width='100%',
        layers=forecast_map_layers,
        legend=True,
        view=forecast_view_options
    )

    context = {
    	'eo_map_options': eo_map_options,
    	'eo_layers': eo_layers,
        'eo_select_options': eo_select_options,
        'eo_years_options': eo_years_options,
        'eo_months_options': eo_months_options,
        'eo_dekads_options': eo_dekads_options,
        #'forecast_map_options': forecast_map_options,
        'forecast_select_options': forecast_select_options,
        'forecast_years_options': forecast_years_options,
        'forecast_months_options': forecast_months_options,
        'forecast_dekads_options': forecast_dekads_options,
        'forecast_layer': forecast_layer,
        'forecast_sld_file': forecast_sld_file,
    }

    return render(request, 'geoserver_app/home.html', context)

#===========================================================================
#===========================================================================

#@login_required()
def map_yields(request):
    """
    Controller for the map page
    """
    print('In map_yields(request) controller')

    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    options = []

    #response = geoserver_engine.list_layers(with_properties=False)
    #print(type(response))
    # dir(response)
    
    #if response['success']:
    #    for layer in response['result']:
    #        tit = layer.title()
    #        if tit.startswith('Yield'):
    #            options.append((layer.title(), layer))
    
    layer = [
    	"geoserver_app:yield_obs_ts_4",
    ]
    
    for l in layer:
    	options.append((l, l))

    select_options = SelectInput(
        display_text='Choose Forecast',
        name='layer',
        multiple=False,
        options=options
    )

    map_layers = []

    if request.POST and 'layer' in request.POST:
        selected_layer = request.POST['layer']
        print('Selected layer type: ')
        print(type(selected_layer))

        selected_layer = 'Yield obs 2015'
        print('selected_layer: ' + selected_layer)
        legend_title = selected_layer.title()
        #print(dir(selected_layer))
        #print('legend_title: ' + legend_title)

        geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'urlxxx': 'https://chc-ewx2.chc.ucsb.edu:8443/geoserver/wms',
                'url': 'http://localhost:8081/geoserver/wms',
                'params': {'LAYERS': selected_layer},
                'serverType': 'geoserver'
            },
            legend_title=legend_title,
            legend_extent=[-114, 36.5, -109, 42.5],
            legend_classes=[
                MVLegendClass('polygon', '> 2.0', fill='#440154'),
                MVLegendClass('polygon', '1.8 - 2.0', fill='#482475'),
                MVLegendClass('polygon', '1.6 - 1.8', fill='#414487'),
                MVLegendClass('polygon', '1.4 - 1.6', fill='#355f8d'),
                MVLegendClass('polygon', '1.2 - 1.4', fill='#2a788e'),
                MVLegendClass('polygon', '1.0 - 1.2', fill='#21908d'),
                MVLegendClass('polygon', '0.8 - 1.0', fill='#22a884'),
                MVLegendClass('polygon', '0.6 - 0.8', fill='#44bf70'),
                MVLegendClass('polygon', '0.4 - 0.6', fill='#7ad151'),
                MVLegendClass('polygon', '0.2 - 0.4', fill='#bddf26'),
                MVLegendClass('polygon', '< 0.2', fill='#fde725'),
			])

        map_layers.append(geoserver_layer)


    view_options = MVView(
        projection='EPSG:4326',
        center=[41, 5],
        zoom=5,
        maxZoom=18,
        minZoom=2
    )

    map_options = MapView(
        height='500px',
        width='100%',
        layers=map_layers,
        legend=True,
        view=view_options
    )

    context = {'map_options': map_options,
               'select_options': select_options}

    return render(request, 'geoserver_app/forecast_map.html', context)


#@login_required()
def create_shapefile(request):
    """
    Controller for the app home page.
    """
    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()
    # print(response)

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=GEOSERVER_URI)

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )

    context = {}

    return render(request, 'geoserver_app/home.html', context)
