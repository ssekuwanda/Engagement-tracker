$(document).ready(function() {
  var row = 0,
    col = 0,
    ncol = 0;
  var sum;
  // sum by row
  $("tr").each(function(rowindex) {
    sum = 0;
    col = 0;
    $(this).find("td").each(function(colindex) {
      col++;
      newval = $(this).find("input").val();
      if (isNaN(newval)) {
        $(this).html(sum);
        if (col > ncol) {
          ncol = col - 1
        }
      } else {
        sum += parseInt(newval);
      }
    });
  });

  // sum by col
  for (col = 1; col < ncol + 1; col++) {
    console.log("column: " + col);
    sum = 0;
    $("tr").each(function(rowindex) {
      $(this).find("td:nth-child(" + col + ")").each(function(rowindex) {
        newval = $(this).find("input").val();
        console.log(newval);
        if (isNaN(newval)) {
          $(this).html(sum);
        } else {
          sum += parseInt(newval);
        }
      });
    });
  }
});
