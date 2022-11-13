import datetime

import boto3

client = boto3.client('ce')

def get_costs(start, end, granularity):
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity=granularity,
        Metrics=[
            'AmortizedCost',
        ],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            },
        ]
    )
    return response

def get_date(days):
    return (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    
def print_costs(response, time_frame, granularity):
    if granularity == 'MONTHLY':
        _extracted_from_print_costs_3(time_frame, 'Month', response)
        for service in response['ResultsByTime'][0]['Groups']:
            if float(service['Metrics']['AmortizedCost']['Amount']) > 0:
                print(f"{service['Keys'][0]:<20} ${float(service['Metrics']['AmortizedCost']['Amount']):<20.2f}")
    else:
        _extracted_from_print_costs_3(time_frame, 'Service', response)
        for service in response['ResultsByTime'][0]['Groups']:
            if float(service['Metrics']['AmortizedCost']['Amount']) > 0:
                print(f"{service['Keys'][0]:<20} ${float(service['Metrics']['AmortizedCost']['Amount'])*10:<20.3f}")
                # print(f"{service['Keys'][0]:<20} ${float(service['Metrics']['AmortizedCost']['Amount']):<20.2f}")

    print("\n\n")


# TODO Rename this here and in `print_costs`
def _extracted_from_print_costs_3(time_frame, arg1, response):
    print(f"{time_frame:<20}")
    print("\n\n")
    print(f"{arg1:<20} {'Cost':<20}")
    response['ResultsByTime'][0]['Groups'].sort(key=lambda x: float(x['Metrics']['AmortizedCost']['Amount']), reverse=True)
    print(f"{'-------':<20} {'----':<20}")

def main():
    # Get costs for the last 30 days
    response = get_costs(get_date(30), get_date(0), 'DAILY')
    print_costs(response, 'Last 30 days', 'DAILY')
    
    # Get costs for the last 12 months
    response = get_costs(get_date(365), get_date(0), 'DAILY')
    print_costs(response, 'Last 12 months', 'DAILY')

    # Get costs for the last 7 days
    response = get_costs(get_date(7), get_date(0), 'DAILY')
    print_costs(response, 'Last 7 days', 'DAILY')

    # Get costs for the last 3 months
    response = get_costs(get_date(90), get_date(0), 'DAILY')
    print_costs(response, 'Last 3 months', 'DAILY')

if __name__ == '__main__':
    main()

