var main = function (){ (


    // https://stackoverflow.com/a/16239245/6655150

    function () {
    // the css we are going to inject
    var css = 'html {-webkit-filter: invert(100%);' +
        '-moz-filter: invert(100%);' +
        '-o-filter: invert(100%);' +
        '-ms-filter: invert(100%); }',

    head = document.getElementsByTagName('head')[0],
    style = document.createElement('style');

    var b = document.getElementsByTagName("body")[0];

    console.log(b.bgColor);
    if (b.bgColor == "black"){
        b.bgColor = "white";
    } else {
        b.bgColor = "black";
    }

    // a hack, so you can "invert back" clicking the bookmarklet again
    if (!window.counter) {
         window.counter = 1;
    } else {
          window.counter ++;
          if (window.counter % 2 == 0) {
               var css ='html {-webkit-filter: invert(0%); -moz-filter:    invert(0%); -o-filter: invert(0%); -ms-filter: invert(0%); }'
           }
    };

    style.type = 'text/css';

    if (style.styleSheet){
        style.styleSheet.cssText = css;
    } else {
        style.appendChild(document.createTextNode(css));
    }

    //injecting the css to the head
    head.appendChild(style);

    var im = document.getElementById("app_logo");

    // https://stackoverflow.com/a/13325820/6655150
    im.style = "-webkit-filter: invert(0); filter: invert(0);"
    if (window.counter % 2 == 1) {
       im.style = "-webkit-filter: invert(1); filter: invert(1);"
    }


}())};

window.onload = function(){
    var dark_theme = document.getElementById("dark_theme");
    dark_theme.onclick = main;
}
