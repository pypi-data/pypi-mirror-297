document$.subscribe(function() {
  var tables = document.querySelectorAll("article table:not([class])") // this line was adjusted
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})