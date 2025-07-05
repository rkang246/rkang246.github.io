/*
Experience accordion
*/
$('.panel-collapse').on('show.bs.collapse', function () {
   $(this).siblings('.panel-heading').addClass('active');
 });

 $('.panel-collapse').on('hide.bs.collapse', function () {
   $(this).siblings('.panel-heading').removeClass('active');
 });


/*
Tagline Cycler
*/
var words = (function(){
  var words = [
      'listening to <strong>chopin</strong>',
      'reading <strong><a href="https://mitpress.mit.edu/books/free-will" target="_blank">free will</a></strong> by mark balaguer',
      'studying <strong>avl trees</strong>',
      'going on a <strong>run</strong>',
      'managing <strong>student debt</strong>',
      'figuring out <strong>responsive</strong> design',
      'attending <strong>office hours</strong> over zoom',
      'discovering that the <strong>real treasure</strong> was the <strong>friends</strong> we made along the way',
      'practicing <strong>Russian</strong> conjugation',

      ],
    el = document.querySelector('.text-cycle'),
    currentIndex,
    currentWord,
    prevWord,
    duration = 4000;

  var _getIndex = function(max, min){
    currentIndex = Math.floor(Math.random() * (max - min + 1)) + min;

    //Generates a random number between beginning and end of words array
    return currentIndex;
  };

  var _getWord = function(index){
    currentWord = words[index];

    return currentWord;
  };

  var _clear = function() {

    setTimeout(function(){
      el.className = 'text-cycle';
    }, duration/4);
  };

  var _toggleWord = function(duration){
    setInterval(function(){
      //Stores value of previous word
      prevWord = currentWord;

      //Generate new current word
      currentWord = words[_getIndex(words.length-1, 0)];

      //Generate new word if prev matches current
      if(prevWord === currentWord){

        currentWord = words[_getIndex(words.length-1, 0)];
      }

      //Swap new value
      el.innerHTML = currentWord;

      //Clear class styles
      _clear();

      //Fade in word
      el.classList.add(
        'js-block',
        'js-fade-in-text-cycle'
        );

    }, duration);
  };

  var _init = function(){
    _toggleWord(duration);
  };

  //Public API
  return {
    init : function(){
      _init();
    }
  };
})();

words.init();


/*
Light Switch
*/
$("#light-switch").click(function(){
  event.preventDefault();

  if ($(this).hasClass("active-light")) { //lights on, turn em off
    $(this).html("lights on.");
    document.documentElement.style.setProperty('--accent-color', '#11c973');
    document.documentElement.style.setProperty('--inactive-color', '#FFF');
    document.documentElement.style.setProperty('--background-color', '#15181a');
    document.documentElement.style.setProperty('--background-color-dark', '#000001');
    document.documentElement.style.setProperty('--body-color', '#949799');
  }
  else { //lights off, turn em on
    $(this).html("lights off.");
    document.documentElement.style.setProperty('--accent-color', '#009640');
    document.documentElement.style.setProperty('--inactive-color', '#0e1111');
    document.documentElement.style.setProperty('--background-color', '#f7f7f7');
    document.documentElement.style.setProperty('--background-color-dark', '#DEDEDE');
    document.documentElement.style.setProperty('--body-color', '#6A6A6A');
  }
   $(this).toggleClass("active-light");
});

/*
Mobile Formatting
*/

/*
Photojournal Modal
*/
// Get the modal
var modal = document.getElementById("modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("img1");
var modalImg = document.getElementById("content-img1");
var captionText = document.getElementById("caption");
img.onclick = function(){
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}