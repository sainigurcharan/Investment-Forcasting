import json
from flask import Flask, render_template, request
import pandas as pd
import numpy as np

# FLASK APP
app = Flask(__name__)

# ROUTE TO RENDER INDEX.HTML
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/calc")
def calc():

    return render_template("calc.html")

@app.route("/portfolio")
def portfolio():
    presentValue = request.args.get('pv')
    investmentValue = request.args.get('iv')
    horizon = request.args.get('yr')
    portfolio = request.args.get('pf')
    regModel = request.args.get('rm')

    print(f"expected_market: {regModel}")
    dataSummary = pd.read_csv(f"historicalSummary/{regModel}Summary.csv")
    dataSummary = dataSummary.set_index("Index")
    dataSummary = dataSummary[['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]

    mean_list = dataSummary.loc[
        'mean', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    mean_list = mean_list.tolist()
    print(mean_list)

    std_list = dataSummary.loc[
        'std', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    std_list = std_list.tolist()
    print(std_list)

    max_list = dataSummary.loc[
        'max', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    max_list = max_list.tolist()
    print(max_list)

    Portfolios = ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']
    big_lst = []
    for x in range(0, 5):
        pv = float(presentValue)
        time_horizon = int(horizon)
        i = mean_list[x]
        additions = float(investmentValue)

        lst = []
        for year in range(time_horizon):
            ending = pv * (1 + i) + additions
            # print(locale.currency(ending, grouping=True))
            pv = ending
            lst.append(pv)

        high_value = lst[-1]
        low_value = high_value * (1 - max_list[x])
        new_lst = [Portfolios[x], high_value, low_value]
        big_lst.append(new_lst)
    data = pd.DataFrame(big_lst)

    data = data.rename(columns={0: 'Portfolios', 1: 'High_Value', 2: 'Low_Value'})

    data = data.set_index('Portfolios')
    #print(f"=> Data: {data.head()}")

    return data.to_json()

@app.route("/eachPortfolio")
def eachPortfolio():
    presentValue = request.args.get('pv')
    investmentValue = request.args.get('iv')
    horizon = request.args.get('yr')
    portfolio = request.args.get('pf')
    regModel = request.args.get('rm')

    print(f"expected_market: {regModel}")
    dataSummary = pd.read_csv(f"historicalSummary/{regModel}Summary.csv")
    dataSummary = dataSummary.set_index("Index")
    dataSummary = dataSummary[['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]

    mean_list = dataSummary.loc[
        'mean', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    mean_list = mean_list.tolist()
    print(mean_list)

    std_list = dataSummary.loc[
        'std', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    std_list = std_list.tolist()
    print(std_list)

    max_list = dataSummary.loc[
        'max', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    max_list = max_list.tolist()
    print(max_list)

    sim = pd.DataFrame()
    iterations = 100

    for x in range(iterations):

        expected_return = dataSummary.iloc[0][portfolio]  # .0867 #Value based on selection
        volatility = dataSummary.iloc[1][portfolio]  # .17 #Value based on selection
        time_horizon = int(horizon)
        pv = float(presentValue)
        annual_investment = float(investmentValue)
        stream = []

        for i in range(time_horizon):
            end = round(pv * (1 + np.random.normal(expected_return, volatility)) + annual_investment, 2)

            stream.append(end)

            pv = end

        sim[x] = stream
    first_ten = list(range(10))
    simOutput = sim[first_ten]
    #print(f"=> Data: {simOutput.head()}")

    return simOutput.to_json()

@app.route("/histogram")
def histogram():
    presentValue = request.args.get('pv')
    investmentValue = request.args.get('iv')
    horizon = request.args.get('yr')
    portfolio = request.args.get('pf')
    regModel = request.args.get('rm')

    print(f"expected_market: {regModel}")
    dataSummary = pd.read_csv(f"historicalSummary/{regModel}Summary.csv")
    dataSummary = dataSummary.set_index("Index")
    dataSummary = dataSummary[['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]

    mean_list = dataSummary.loc[
        'mean', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    mean_list = mean_list.tolist()
    print(mean_list)

    std_list = dataSummary.loc[
        'std', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    std_list = std_list.tolist()
    print(std_list)

    max_list = dataSummary.loc[
        'max', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    max_list = max_list.tolist()
    print(max_list)

    simH = pd.DataFrame()
    iterations = 1000
    for x in range(iterations):

        expected_return = dataSummary.iloc[0][portfolio]  # .0867 #Value based on selection
        volatility = dataSummary.iloc[1][portfolio]  # .17 #Value based on selection
        time_horizon = int(horizon)
        pv = float(presentValue)
        annual_investment = float(investmentValue)
        stream = []

        for i in range(time_horizon):
            end = round(pv * (1 + np.random.normal(expected_return, volatility)) + annual_investment, 2)

            stream.append(end)

            pv = end

        simH[x] = stream

    ending_values = simH.loc[time_horizon - 1]
    prob_of_success = (len(ending_values[ending_values > 4000000]) / len(ending_values)) * 100

    return ending_values.to_json()

@app.route("/probOfSuccess")
def probOfSuccess():
    presentValue = request.args.get('pv')
    investmentValue = request.args.get('iv')
    horizon = request.args.get('yr')
    portfolio = request.args.get('pf')
    endAmount = request.args.get('ps')
    regModel = request.args.get('rm')

    print(f"expected_market: {regModel}")
    dataSummary = pd.read_csv(f"historicalSummary/{regModel}Summary.csv")
    dataSummary = dataSummary.set_index("Index")
    dataSummary = dataSummary[['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]

    mean_list = dataSummary.loc[
        'mean', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    mean_list = mean_list.tolist()
    print(mean_list)

    std_list = dataSummary.loc[
        'std', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    std_list = std_list.tolist()
    print(std_list)

    max_list = dataSummary.loc[
        'max', ['Very_Conservative', 'Conservative', 'Moderate', 'Aggressive', 'Very_Aggressive']]
    max_list = max_list.tolist()
    print(max_list)

    simP = pd.DataFrame()
    iterations = 1000
    for x in range(iterations):

        expected_return = dataSummary.iloc[0][portfolio]  # .0867 #Value based on selection
        volatility = dataSummary.iloc[1][portfolio]  # .17 #Value based on selection
        time_horizon = int(horizon)
        pv = float(presentValue)
        annual_investment = float(investmentValue)
        stream = []

        for i in range(time_horizon):
            end = round(pv * (1 + np.random.normal(expected_return, volatility)) + annual_investment, 2)

            stream.append(end)

            pv = end

        simP[x] = stream

    ending_values = simP.loc[time_horizon - 1]
    prob_of_success = (len(ending_values[ending_values > float(endAmount)]) / len(ending_values)) * 100
    prob_of_success = "{0:.2f}".format(prob_of_success)
    pString = f"Your probability of success is {prob_of_success}%"
    pString = json.dumps(pString)
    return pString

if __name__ == "__main__":
    app.run(debug= True)