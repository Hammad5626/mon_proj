document.addEventListener('DOMContentLoaded', function() {
  let contextData = contextJson;
  let profitList = contextData.profit_list;
  let netProfitList = contextData.net_profit_list;
  let typeList = contextData.type_list;
  let openingTimeList = contextData.time_list;
  let totalBalance = [profitList[0]];
  let monthlyData = {};
  let yearlyData = {};
  let currentBalance = 0;

  for (let i = 0; i < profitList.length; i++) {
    if (i !== 0 && typeList[i] !== "Balance") {
      currentBalance = totalBalance[i - 1] + netProfitList[i];
      totalBalance.push(currentBalance);
    }
    else if(i !== 0 && typeList[i] === "Balance") {
      currentBalance = totalBalance[i - 1] + profitList[i];
      totalBalance.push(currentBalance);
    }
  }
  let year =0;
  for (let i = 0; i < openingTimeList.length; i++) {
    let dateComponents = openingTimeList[i].split('-');
    let month = dateComponents[1];
    year = dateComponents[0];
    let currentBalance = totalBalance[i];
    let monthYear = month + '-' + year;
    
    
    if (monthYear in monthlyData) {
      if (i < openingTimeList.length - 2 && month === openingTimeList[i+1].split('-')[1] && typeList[i+1] === "Balance"){
        let result = ((currentBalance - monthlyData[monthYear].initialValue) / monthlyData[monthYear].initialValue) *100;
        result = (result / 100) +1;
        monthlyData[monthYear].iterator *= result;
      }
      else if (typeList[i] === "Balance"){
        monthlyData[monthYear].initialValue = currentBalance;
      }
      monthlyData[monthYear].finalValue = currentBalance;
    } else {
      monthlyData[monthYear] = {
        initialValue: currentBalance,
        finalValue: 0,
        iterator: 1
      };
    }
  }

  let yearlyPercentage = 1;
  // Calculate the percentage growth for each month
  let monthlyTableBody = document.querySelector('tbody');
  let monthYearArray = Object.keys(monthlyData);
  for (let i = 0; i < monthYearArray.length; i++) {
    let monthYear = monthYearArray[i];
    let [month, year] = monthYear.split('-');
    let initialValue = monthlyData[monthYear].initialValue;
    let finalValue = monthlyData[monthYear].finalValue;
    let iterator = monthlyData[monthYear].iterator;
    let percentageOfMonth = 0;
    let result = 0;

    if (initialValue !== 0) {
      result = ((finalValue - initialValue) / initialValue) * 100;
      result = (result / 100) +1;
      iterator *= result;
      percentageOfMonth = (iterator - 1) * 100;
      yearlyPercentage *= (percentageOfMonth/100) +1;
    }

    let row = document.createElement('tr');
    let yearMonthCell = document.createElement('td');
    let percentageOfMonthCell = document.createElement('td');

    yearMonthCell.textContent = year + '-' + month;
    percentageOfMonthCell.textContent = percentageOfMonth.toFixed(2) + '%';

    row.appendChild(yearMonthCell);
    row.appendChild(percentageOfMonthCell);

    monthlyTableBody.appendChild(row);
  }

  // Create yearly data array
  let yearlyTableBody = document.querySelectorAll('tbody')[1];
    yearlyPercentage = (yearlyPercentage - 1)*100;
    let row = document.createElement('tr');

    let yearCell = document.createElement('td');
    yearCell.textContent = year;

    let percentageCell = document.createElement('td');
    percentageCell.textContent = yearlyPercentage.toFixed(2) + '%';

    row.appendChild(yearCell);
    row.appendChild(percentageCell);

    yearlyTableBody.appendChild(row);
});