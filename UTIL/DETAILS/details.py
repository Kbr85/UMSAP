#region ----------------------------------------------------------> UMSAP File
"""The umsap file contains the output from UMSAP. The file is json formated 
and contains the sections described below."""
#endregion -------------------------------------------------------> UMSAP File

#region ----------------------------------------> Correlation Analysis section
"""The section Correlation Analysis in an UMSAP File has the following 
structure:"""

{
	'Correlation-Analysis' : {
		'20210324-165609': {
			'V' : { # UMSAP version
				'Version': version,
			},
			'I' : { # Values as given by the user
				'iFile'     : 'input file path',
				'oFolder'   : 'output folder path',
				'NormMethod': 'normalization method',
				'CorrMethod': 'correlation method',
				'Column'    : [selected columns as integers],
			},
			'CI': { # Ready to use values
				'iFile'     : 'input file path',
				'oFolder'   : 'output folder path',
				'NormMethod': 'normalization method',
				'CorrMethod': 'correlation method',
				'Column'    : [selected columns as integers],
			},
			'R' : pd.DataFrame (dict) with the correlation coefficients,
		}
	}
}

"""
The date-time stamp ('20210324-165609') indicates when the analysis was 
performed. 

The Dataframe in 'R' has the following structure:

              Intensity 01  Intensity 02  Intensity 03  Intensity 04  Intensity 05
Intensity 01      1.000000      0.771523      0.162302      0.135884      0.565985
Intensity 02      0.771523      1.000000      0.190120      0.110859      0.588783
Intensity 03      0.162302      0.190120      1.000000      0.775442     -0.010327
Intensity 04      0.135884      0.110859      0.775442      1.000000      0.010221
Intensity 05      0.565985      0.588783     -0.010327      0.010221      1.000000

The index and column names are the name of the selected columns in the Data File.
"""
#endregion -------------------------------------> Correlation Analysis section

