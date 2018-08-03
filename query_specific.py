# Copyright 2018 BACnet Gateway.  All rights reserved.

try:
    import argparse
    import pandas as pd
    from bacnet_gateway_requests import get_value_and_units
    import time as currentDT

    # Get hostname and port of BACnet Gateway
    parser = argparse.ArgumentParser( description='Test BACnet Gateway', add_help=False )
    parser.add_argument( '-h', dest='hostname' )
    parser.add_argument( '-p', dest='port' )
    parser.add_argument( '-w', dest='wing' )
    parser.add_argument( '-f', dest='floor' )
    args = parser.parse_args()

    # Read spreadsheet into a dataframe.
    # Each row contains the following:
    #   - Location
    #   - Instance ID of CO2 sensor
    #   - Instance ID of temperature sensor
    df = pd.read_csv( 'csv/ahs_air.csv', na_filter=False, comment='#' )
    locations = pd.read_csv( 'csv/ahs_air_wing.csv', na_filter=False, comment='#')

    output = open("csv/ahs_air_specific_output.csv", "w")

    print("Getting data for wing " + args.wing + " on floor " + str(int(args.floor) + 1))

    # Output column headings
    print( 'Location,\tTemperature,\tTemperature Units,\tCO2,\tCO2 Units,\tTimestamp' )
    output.write( ',Timestamp,Location,Temperature,Temperature Units,CO2,CO2 Units,\n' )

    # Iterate over the rows of the dataframe, getting temperature and CO2 values for each location
    for index, row in df.iterrows():

        # check if it is on the correct wing and floor
        if locations['Wing'][index] != args.wing or int(locations['Floor'][index]) != int(args.floor) + 1:
            continue;

        # Retrieve data
        temp_value, temp_units = get_value_and_units( row['Facility'], row['Temperature'], args.hostname, args.port )
        co2_value, co2_units = get_value_and_units( row['Facility'], row['CO2'], args.hostname, args.port )

        # Prepare to print
        temp_value = int( temp_value ) if temp_value else ''
        temp_units = temp_units if temp_units else ''
        co2_value = int( co2_value ) if co2_value else ''
        co2_units = co2_units if co2_units else ''

        # Output CSV format
        print( '{0},\t\t{1},\t\t\t\t{2},\t\t\t\t{3},\t{4},\t{5},'.format( row['Label'], temp_value, temp_units, co2_value, co2_units, currentDT.strftime("%m/%d/%Y %H:%M:%S") ) )
        output.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(index, currentDT.strftime("%m/%d/%Y %H:%M:%S"), row['Label'], temp_value, temp_units, co2_value, co2_units))

except KeyboardInterrupt:
    output.close()
    print('Bye')
    import sys
    sys.exit()

output.close()