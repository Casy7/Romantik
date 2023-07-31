

$('#responsiblePersonSelector').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
  $('#responsiblePerson')[0].value = $('#responsiblePersonSelector')[0][clickedIndex].dataset.tokens;
});

function beauty_date_interval(str_date1, str_date2) {
  date1 = new Date(str_date1);
  date2 = new Date(str_date2);
  months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
  result = '';
  result += date1.getDate().toString() + ' ';

  if ([date1.getDate(), date1.getMonth(), date1.getFullYear()] == [date2.getDate(), date2.getMonth(), date2.getFullYear()]) {
    result += months[date1.getMonth()];
  }
  else {
    if (date1.getMonth() == date2.getMonth()) {
      result += '- ' + date2.getDate().toString() + ' ' + months[date1.getMonth()];
    }
    else {
      result += months[date1.getMonth()] + ' - ' +
        date2.getDate().toString() + ' ' + months[date2.getMonth()];
    }
  }
  let now = new Date();
  if (date1.getFullYear() != now.getFullYear()) {
    result += ', ' + date1.getFullYear().toString();
  }

  return result;
}
