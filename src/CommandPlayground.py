SetupFor = {
    "MeasurementType":"Unconfigured",
    "Range":"Unconfigured",
    "Resolution":"Unconfigured",
}

supported_commands = {
    "CONFigure": {
        "VOLTage": {
            "DC": {
                "Range": ["MIN", "MAX", "AUTO"],
                "Resolution": ["MIN", "MAX", "DEF"],
            },
        },
        "CURRent": {
            "AC": {
                "Range": ["MIN", "MAX", "AUTO", "10mA", "100mA", "1A", "2A"],
                "Resolution": ["MIN", "MAX", "DEF"],
            },
        },
        "RESistance": {
            "Range": ["MIN", "MAX", "AUTO", "100", "1k", "10k", "100k", "1M", "10M", "100M"],
            "Resolution": ["MIN", "MAX", "DEF", "3.00e–5", "2.00e–5", "1.00e–5", "5.00e–6", "2.00e–6", "1.50e–6"],
        }
    }
}
