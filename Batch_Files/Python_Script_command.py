import subprocess
from datetime import datetime

scripts = [ 'ETL_Scripts/clear_directory_archive.py',
            'ETL_Scripts/fetching_data.py',
            'ETL_Scripts/compile_and_group_data.py',
            'ETL_Scripts/log_historical_changes.py',
            'Email_Scripts/moving_average_cross_email.py',
]

python_dir = 'C:/Users/us52873/Documents/Personal/investing/'

for script in scripts:
    print('Start: ', script)

    try:
        result = subprocess.run(['python', python_dir + script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        decoded_results = result.stdout.decode('utf-8')

    except subprocess.CalledProcessError as e:
        std_out = str(e.stdout.decode('utf-8'))
        std_err = str(e.stderr.decode('utf-8'))
        decoded_results = f'{std_out}\n{std_err}\n'

    except Exception as e2:
        decoded_results = str(e2)

    print(decoded_results)
