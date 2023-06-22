document.addEventListener('DOMContentLoaded', function() {
    let contextData = contextJson;
    let profitList = contextData.profit_list;
    let netProfitList = contextData.net_profit_list;
    let typeList = contextData.type_list;
    let openingTimeList = contextData.time_list;
    let totalBalance = [profitList[0]];
    let monthlyData = {};
    let yearlyData = {};
    let totalProfit = 0;
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

    for (let i = 0; i < openingTimeList.length; i++) {
      let dateComponents = openingTimeList[i].split('-');
      let month = dateComponents[1];
      let year = dateComponents[0];
      let profit = 0;
      if (typeList[i] !== "Balance"){profit = netProfitList[i];}
      else{profit = profitList[i]}
      let currentBalance = totalBalance[i];
      let monthYear = month + '-' + year;
      
      if (monthYear in monthlyData) {
        monthlyData[monthYear].finalValue = currentBalance;
      } else {
        monthlyData[monthYear] = {
          initialValue: currentBalance,
          finalValue: 0
        };
      }

      // Update yearly data
      if (year in yearlyData) {
        yearlyData[year] += profit;
      } else {
        yearlyData[year] = profit;
      }

      totalProfit += profit;
    }

    // Calculate the percentage growth for each month
    let monthlyTableBody = document.querySelector('tbody');
    let monthYearArray = Object.keys(monthlyData);
    for (let i = 0; i < monthYearArray.length; i++) {
      let monthYear = monthYearArray[i];
      let [month, year] = monthYear.split('-');
      let initialValue = monthlyData[monthYear].initialValue;
      let finalValue = monthlyData[monthYear].finalValue;
      let profitOfMonth = 0;
      let percentageOfMonth = 0;

      if (initialValue !== 0) {
        percentageOfMonth = ((finalValue - initialValue) / initialValue) * 100;
        profitOfMonth = finalValue - initialValue;
      }

      let row = document.createElement('tr');
      let yearMonthCell = document.createElement('td');
      let profitOfMonthCell = document.createElement('td');
      let percentageOfMonthCell = document.createElement('td');

      yearMonthCell.textContent = year + '-' + month;
      profitOfMonthCell.textContent = profitOfMonth;
      percentageOfMonthCell.textContent = percentageOfMonth.toFixed(2) + '%';

      row.appendChild(yearMonthCell);
      row.appendChild(profitOfMonthCell);
      row.appendChild(percentageOfMonthCell);

      monthlyTableBody.appendChild(row);
    }

    // Create yearly data array
    let yearlyTableBody = document.querySelectorAll('tbody')[1];
    for (let year in yearlyData) {
      let profit = yearlyData[year];
      let percentage = ((profit / totalProfit) * 100).toFixed(2);

      let row = document.createElement('tr');

      let yearCell = document.createElement('td');
      yearCell.textContent = year;

      let profitCell = document.createElement('td');
      profitCell.textContent = profit;

      let percentageCell = document.createElement('td');
      percentageCell.textContent = percentage + '%';

      row.appendChild(yearCell);
      row.appendChild(profitCell);
      row.appendChild(percentageCell);

      yearlyTableBody.appendChild(row);
    }
  });