var words = (function(){
  var words = [
      'reading <strong><a href="https://mitpress.mit.edu/books/free-will" target="_blank">free will</a></strong> by mark balaguer',
      'studying <strong>avl trees</strong>',
      'staying <strong>quarantined</strong> from covid-19',
      'listening to <strong><a href="https://crimejunkiepodcast.com/" target="_blank">crime junkie</a></strong>',
      'staying <strong>hydrated</strong>',
      'going on a <strong>run</strong>',

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
