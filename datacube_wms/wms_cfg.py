# Static config for the wms metadata.

response_cfg = {
    "Access-Control-Allow-Origin": "*",  # CORS header
}

service_cfg = {
    # Required config
    "title": "WMS server for Australian Landsat Datacube",
    "url": "http://9xjfk12.nexus.csiro.au/datacube_wms",
    "published_CRSs": {
        "EPSG:3857": {  # Web Mercator
            "geographic": False,
            "horizontal_coord": "x",
            "vertical_coord": "y",
        },
        "EPSG:4326": {  # WGS-84
            "geographic": True,
        },
        "EPSG:3577": {  # GDA-94, internal representation
            "geographic": False,
            "horizontal_coord": "easting",
            "vertical_coord": "northing",
        },
    },

    # Technically optional config, but strongly recommended
    "layer_limit": 1,
    "max_width": 512,
    "max_height": 512,

    # Optional config - may be set to blank/empty
    "abstract": """Historic Landsat imagery for Australia.""",
    "keywords": [
        "landsat",
        "australia",
        "time-series",
    ],
    "contact_info": {
        "person": "David Gavin",
        "organisation": "Geoscience Australia",
        "position": "Technical Lead",
        "address": {
            "type": "postal",
            "address": "GPO Box 378",
            "city": "Canberra",
            "state": "ACT",
            "postcode": "2906",
            "country": "Australia",
        },
        "telephone": "+61 2 1234 5678",
        "fax": "+61 2 1234 6789",
        "email": "test@example.com",
    },
    "fees": "",
    "access_constraints": "",
}

layer_cfg = [
    # Layer Config is a list of platform configs
        {
        # Name and title of the platform layer.
        # Platform layers are not mappable. The name is for internal server use only.
        "name": "Sentinel-2B-NRT",
        "title": "Sentinel-2B-NRT",
        "abstract": "Sentinel 2 Beta NRT data",

        # Products available for this platform.
        # For each product, the "name" is the Datacube name, and the label is used
        # to describe the label to end-users.
        "products": [
            {
                # Included as a keyword  for the layer
                "label": "NBAR",
                # Included as a keyword  for the layer
                "type": "ard",
                # Included as a keyword  for the layer
                "variant": "MSI",
                # The WMS name for the layer
                "name": "s2b_nrt_granule_nbar",
                # The Datacube name for the associated data product
                "product_name": "s2b_nrt_granule",
                # The Datacube name for the associated pixel-quality product (optional)
                # The name of the associated Datacube pixel-quality product
                # "pq_dataset": "s2b_nrt_granule",
                # The name of the measurement band for the pixel-quality product
                # (Only required if pq_dataset is set)
                # "pq_band": "pixel_quality",
                # Min zoom factor - sets the zoom level where the cutover from indicative polygons
                # to actual imagery occurs.
                "min_zoom_factor": 500.0,
                # The fill-colour of the indicative polygons when zoomed out.
                # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
                "zoomed_out_fill_colour": [150, 180, 200, 160],
                # Time Zone.  In hours added to UTC (maybe negative)
                # Used for rounding off scene times to a date.
                # 9 is good value for imagery of Australia.
                "time_zone": 9,
                # Extent mask function
                # Determines what portions of dataset is potentially meaningful data.
                "extent_mask_func": lambda data, band: (data[band] != data[band].attrs['nodata']),
                # Flags listed here are ignored in GetFeatureInfo requests.
                # (defaults to empty list)
                "ignore_info_flags": [],
                # Styles.
                #
                # See band_mapper.py
                #
                # The various available spectral bands, and ways to combine them
                # into a single rgb image.
                # The examples here are ad hoc
                #
                "styles": [
                    # Examples of styles which are linear combinations of the available spectral bands.
                    #
                    {
                        "name": "simple_rgb",
                        "title": "Simple RGB",
                        "abstract": "Simple true-colour image, using the red, green and blue bands",
                        "components": {
                            "red": {
                                "nbar_red": 1.0
                            },
                            "green": {
                                "nbar_green": 1.0
                            },
                            "blue": {
                                "nbar_blue": 1.0
                            }
                        },
                        # Used to clip off very bright areas.
                        "scale_factor": 12.0
                    },
                    {
                        "name": "extended_rgb",
                        "title": "Extended RGB",
                        "abstract": "Extended true-colour image, incorporating the coastal aerosol band",
                        "components": {
                            "red": {
                                "nbar_red": 1.0
                            },
                            "green": {
                                 "nbar_green": 1.0
                            },
                            "blue": {
                                 "nbar_blue": 0.6,
                                 "nbar_coastal_aerosol": 0.4
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "wideband",
                        "title": "Wideband false-colour",
                        "abstract": "False-colour image, incorporating all available spectral bands",
                        "components": {
                            "red": {
                                "nbar_swir_3": 0.255,
                                "nbar_swir_2": 0.45,
                                "nbar_nir_1": 0.255,
                            },
                            "green": {
                                "nbar_nir_1": 0.255,
                                "nbar_red": 0.45,
                                "nbar_green": 0.255,
                            },
                            "blue": {
                                "nbar_green": 0.255,
                                "nbar_blue": 0.45,
                                "nbar_coastal_aerosol": 0.255,
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "infra_red",
                        "title": "False colour multi-band infra-red",
                        "abstract": "Simple false-colour image, using the near and short-wave infra-red bands",
                        "components": {
                            "red": {
                                "nbar_swir_2": 1.0
                            },
                            "green": {
                                "nbar_swir_3": 1.0
                            },
                            "blue": {
                                "nbar_nir_1": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "aerosol",
                        "title": "Spectral band 1 - Coastal aerosol",
                        "abstract": "Coastal aerosol band, approximately 435nm to 450nm",
                        "components": {
                            "red": {
                                "nbar_coastal_aerosol": 1.0
                            },
                            "green": {
                                "nbar_coastal_aerosol": 1.0
                            },
                            "blue": {
                                "nbar_coastal_aerosol": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "blue",
                        "title": "Spectral band 2 - Blue",
                        "abstract": "Blue band, approximately 453nm to 511nm",
                        "components": {
                            "red": {
                                "nbar_blue": 1.0
                            },
                            "green": {
                                "nbar_blue": 1.0
                            },
                            "blue": {
                                "nbar_blue": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "green",
                        "title": "Spectral band 3 - Green",
                        "abstract": "Green band, approximately 534nm to 588nm",
                        "components": {
                            "red": {
                                "nbar_green": 1.0
                            },
                            "green": {
                                "nbar_green": 1.0
                            },
                            "blue": {
                                "nbar_green": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "red",
                        "title": "Spectral band 4 - Red",
                        "abstract": "Red band, roughly 637nm to 672nm",
                        "components": {
                            "red": {
                                "nbar_red": 1.0
                            },
                            "green": {
                                "nbar_red": 1.0
                            },
                            "blue": {
                                "nbar_red": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "nir",
                        "title": "Spectral band 5 - Near infra-red",
                        "abstract": "Near infra-red band, roughly 853nm to 876nm",
                        "components": {
                            "red": {
                                "nbar_nir_1": 1.0
                            },
                            "green": {
                                "nbar_nir_1": 1.0
                            },
                            "blue": {
                                "nbar_nir_1": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "narrow_nir",
                        "title": "Narrow band Near Infra-Red",
                        "abstract": "Near infra-red band, centred on 865nm",
                        "components": {
                            "red": {
                                "nbar_nir_2": 1.0
                            },
                            "green": {
                                "nbar_nir_2": 1.0
                            },
                            "blue": {
                                "nbar_nir_2": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "swir1",
                        "title": "Spectral band 6 - Short wave infra-red 1",
                        "abstract": "Short wave infra-red band 1, roughly 1575nm to 1647nm",
                        "components": {
                            "red": {
                                "nbar_swir_2": 1.0
                            },
                            "green": {
                                "nbar_swir_2": 1.0
                            },
                            "blue": {
                                "nbar_swir_2": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "swir2",
                        "title": "Spectral band 7 - Short wave infra-red 2",
                        "abstract": "Short wave infra-red band 2, roughly 2117nm to 2285nm",
                        "components": {
                            "red": {
                                "nbar_swir_3": 1.0
                            },
                            "green": {
                                "nbar_swir_3": 1.0
                            },
                            "blue": {
                                "nbar_swir_3": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    #
                    # Examples of non-linear heat-mapped styles.
                    {
                        "name": "ndvi",
                        "title": "NDVI",
                        "abstract": "Normalised Difference Vegetation Index - a derived index that correlates well with the existence of vegetation",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbar_nir_1"] - data["nbar_red"]) / (data["nbar_nir_1"] + data["nbar_red"]),
                        "needed_bands": ["nbar_red", "nbar_nir_1"],
                        # Areas where the index_function returns outside the range are masked.
                        "range": [0.0, 1.0],
                    },
                    {
                        "name": "ndwi",
                        "title": "NDWI",
                        "abstract": "Normalised Difference Water Index - a derived index that correlates well with the existence of water",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbar_green"] - data["nbar_nir_1"]) / (data["nbar_nir_1"] + data["nbar_green"]),
                        "needed_bands": ["nbar_green", "nbar_nir_1"],
                        "range": [0.0, 1.0],
                    },
                    {
                        "name": "ndbi",
                        "title": "NDBI",
                        "abstract": "Normalised Difference Buildup Index - a derived index that correlates with the existence of urbanisation",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbar_swir_3"] - data["nbar_nir_1"]) / (data["nbar_swir_3"] + data["nbar_nir_1"]),
                        "needed_bands": ["nbar_swir_3", "nbar_nir_1"],
                        "range": [0.0, 1.0],
                    },
                    # Mask layers - examples of how to display raw pixel quality data.
                    # This works by creatively mis-using the Heatmap style class.
                    # Hybrid style - mixes a linear mapping and a heat mapped index
                    {
                        "name": "rgb_ndvi",
                        "title": "NDVI plus RGB",
                        "abstract": "Normalised Difference Vegetation Index (blended with RGB) - a derived index that correlates well with the existence of vegetation",
                        "component_ratio": 0.6,
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbar_nir_1"] - data["nbar_red"]) / (data["nbar_nir_1"] + data["nbar_red"]),
                        "needed_bands": ["nbar_red", "nbar_nir_1"],
                        # Areas where the index_function returns outside the range are masked.
                        "range": [0.0, 1.0],
                        "components": {
                            "red": {
                                "nbar_red": 1.0
                            },
                            "green": {
                                "nbar_green": 1.0
                            },
                            "blue": {
                                "nbar_blue": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    }
                ],
                # Default style (if request does not specify style)
                # MUST be defined in the styles list above.
                # (Looks like Terria assumes this is the first style in the list, but this is
                #  not required by the standard.)
                "default_style": "simple_rgb",
            },

            {
                # Included as a keyword  for the layer
                "label": "NBAR-T",
                # Included as a keyword  for the layer
                "type": "nrt",
                # Included as a keyword  for the layer
                "variant": "MSI",
                # The WMS name for the layer
                "name": "s2b_nrt_granule_nbar_t",
                # The Datacube name for the associated data product
                "product_name": "s2b_nrt_granule",
                # The Datacube name for the associated pixel-quality product (optional)
                # The name of the associated Datacube pixel-quality product
                # "pq_dataset": "s2b_nrt_granule",
                # The name of the measurement band for the pixel-quality product
                # (Only required if pq_dataset is set)
                # "pq_band": "pixel_quality",
                # Min zoom factor - sets the zoom level where the cutover from indicative polygons
                # to actual imagery occurs.
                "min_zoom_factor": 500.0,
                # The fill-colour of the indicative polygons when zoomed out.
                # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
                "zoomed_out_fill_colour": [150, 180, 200, 160],
                # Time Zone.  In hours added to UTC (maybe negative)
                # Used for rounding off scene times to a date.
                # 9 is good value for imagery of Australia.
                "time_zone": 9,
                # Extent mask function
                # Determines what portions of dataset is potentially meaningful data.
                "extent_mask_func": lambda data, band: (data[band] != data[band].attrs['nodata']),
                # Flags listed here are ignored in GetFeatureInfo requests.
                # (defaults to empty list)
                "ignore_info_flags": [],
                # Styles.
                #
                # See band_mapper.py
                #
                # The various available spectral bands, and ways to combine them
                # into a single rgb image.
                # The examples here are ad hoc
                #
                "styles": [
                    # Examples of styles which are linear combinations of the available spectral bands.
                    #
                    {
                        "name": "simple_rgb",
                        "title": "Simple RGB",
                        "abstract": "Simple true-colour image, using the red, green and blue bands",
                        "components": {
                            "red": {
                                "nbart_red": 1.0
                            },
                            "green": {
                                "nbart_green": 1.0
                            },
                            "blue": {
                                "nbart_blue": 1.0
                            }
                        },
                        # Used to clip off very bright areas.
                        "scale_factor": 12.0
                    },
                    {
                        "name": "extended_rgb",
                        "title": "Extended RGB",
                        "abstract": "Extended true-colour image, incorporating the coastal aerosol band",
                        "components": {
                            "red": {
                                "nbart_red": 1.0
                            },
                            "green": {
                                 "nbart_green": 1.0
                            },
                            "blue": {
                                 "nbart_blue": 0.6,
                                 "nbart_coastal_aerosol": 0.4
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "wideband",
                        "title": "Wideband false-colour",
                        "abstract": "False-colour image, incorporating all available spectral bands",
                        "components": {
                            "red": {
                                "nbart_swir_3": 0.255,
                                "nbart_swir_2": 0.45,
                                "nbart_nir_1": 0.255,
                            },
                            "green": {
                                "nbart_nir_1": 0.255,
                                "nbart_red": 0.45,
                                "nbart_green": 0.255,
                            },
                            "blue": {
                                "nbart_green": 0.255,
                                "nbart_blue": 0.45,
                                "nbart_coastal_aerosol": 0.255,
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "infra_red",
                        "title": "False colour multi-band infra-red",
                        "abstract": "Simple false-colour image, using the near and short-wave infra-red bands",
                        "components": {
                            "red": {
                                "nbart_swir_2": 1.0
                            },
                            "green": {
                                "nbart_swir_3": 1.0
                            },
                            "blue": {
                                "nbart_nir_1": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "aerosol",
                        "title": "Spectral band 1 - Coastal aerosol",
                        "abstract": "Coastal aerosol band, approximately 435nm to 450nm",
                        "components": {
                            "red": {
                                "nbart_coastal_aerosol": 1.0
                            },
                            "green": {
                                "nbart_coastal_aerosol": 1.0
                            },
                            "blue": {
                                "nbart_coastal_aerosol": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "blue",
                        "title": "Spectral band 2 - Blue",
                        "abstract": "Blue band, approximately 453nm to 511nm",
                        "components": {
                            "red": {
                                "nbart_blue": 1.0
                            },
                            "green": {
                                "nbart_blue": 1.0
                            },
                            "blue": {
                                "nbart_blue": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "green",
                        "title": "Spectral band 3 - Green",
                        "abstract": "Green band, approximately 534nm to 588nm",
                        "components": {
                            "red": {
                                "nbart_green": 1.0
                            },
                            "green": {
                                "nbart_green": 1.0
                            },
                            "blue": {
                                "nbart_green": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "red",
                        "title": "Spectral band 4 - Red",
                        "abstract": "Red band, roughly 637nm to 672nm",
                        "components": {
                            "red": {
                                "nbart_red": 1.0
                            },
                            "green": {
                                "nbart_red": 1.0
                            },
                            "blue": {
                                "nbart_red": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "nir",
                        "title": "Spectral band 5 - Near infra-red",
                        "abstract": "Near infra-red band, roughly 853nm to 876nm",
                        "components": {
                            "red": {
                                "nbart_nir_1": 1.0
                            },
                            "green": {
                                "nbart_nir_1": 1.0
                            },
                            "blue": {
                                "nbart_nir_1": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "narrow_nir",
                        "title": "Narrow band Near Infra-Red",
                        "abstract": "Near infra-red band, centred on 865nm",
                        "components": {
                            "red": {
                                "nbart_nir_2": 1.0
                            },
                            "green": {
                                "nbart_nir_2": 1.0
                            },
                            "blue": {
                                "nbart_nir_2": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "swir1",
                        "title": "Spectral band 6 - Short wave infra-red 1",
                        "abstract": "Short wave infra-red band 1, roughly 1575nm to 1647nm",
                        "components": {
                            "red": {
                                "nbart_swir_2": 1.0
                            },
                            "green": {
                                "nbart_swir_2": 1.0
                            },
                            "blue": {
                                "nbart_swir_2": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    {
                        "name": "swir2",
                        "title": "Spectral band 7 - Short wave infra-red 2",
                        "abstract": "Short wave infra-red band 2, roughly 2117nm to 2285nm",
                        "components": {
                            "red": {
                                "nbart_swir_3": 1.0
                            },
                            "green": {
                                "nbart_swir_3": 1.0
                            },
                            "blue": {
                                "nbart_swir_3": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    },
                    #
                    # Examples of non-linear heat-mapped styles.
                    {
                        "name": "ndvi",
                        "title": "NDVI",
                        "abstract": "Normalised Difference Vegetation Index - a derived index that correlates well with the existence of vegetation",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbart_nir_1"] - data["nbart_red"]) / (data["nbart_nir_1"] + data["nbart_red"]),
                        "needed_bands": ["nbart_red", "nbart_nir_1"],
                        # Areas where the index_function returns outside the range are masked.
                        "range": [0.0, 1.0],
                    },
                    {
                        "name": "ndwi",
                        "title": "NDWI",
                        "abstract": "Normalised Difference Water Index - a derived index that correlates well with the existence of water",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbart_green"] - data["nbart_nir_1"]) / (data["nbart_nir_1"] + data["nbart_green"]),
                        "needed_bands": ["nbart_green", "nbart_nir_1"],
                        "range": [0.0, 1.0],
                    },
                    {
                        "name": "ndbi",
                        "title": "NDBI",
                        "abstract": "Normalised Difference Buildup Index - a derived index that correlates with the existence of urbanisation",
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbart_swir_3"] - data["nbart_nir_1"]) / (data["nbart_swir_3"] + data["nbart_nir_1"]),
                        "needed_bands": ["nbart_swir_3", "nbart_nir_1"],
                        "range": [0.0, 1.0],
                    },
                    # Mask layers - examples of how to display raw pixel quality data.
                    # This works by creatively mis-using the Heatmap style class.
                    # Hybrid style - mixes a linear mapping and a heat mapped index
                    {
                        "name": "rgb_ndvi",
                        "title": "NDVI plus RGB",
                        "abstract": "Normalised Difference Vegetation Index (blended with RGB) - a derived index that correlates well with the existence of vegetation",
                        "component_ratio": 0.6,
                        "heat_mapped": True,
                        "index_function": lambda data: (data["nbart_nir_1"] - data["nbart_red"]) / (data["nbart_nir_1"] + data["nbart_red"]),
                        "needed_bands": ["nbart_red", "nbart_nir_1"],
                        # Areas where the index_function returns outside the range are masked.
                        "range": [0.0, 1.0],
                        "components": {
                            "red": {
                                "nbart_red": 1.0
                            },
                            "green": {
                                "nbart_green": 1.0
                            },
                            "blue": {
                                "nbart_blue": 1.0
                            }
                        },
                        "scale_factor": 12.0
                    }
                ],
                # Default style (if request does not specify style)
                # MUST be defined in the styles list above.
                # (Looks like Terria assumes this is the first style in the list, but this is
                #  not required by the standard.)
                "default_style": "simple_rgb",
            },
        ],
    },
]

