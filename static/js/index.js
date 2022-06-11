var menuItems = $(".menu_item");
console.log(menuItems);

$(document).ready(function(){
  console.log(menuItems.parent());
  console.log(menuItems[0]);
  console.log(menuItems[0].parentNode);

});
