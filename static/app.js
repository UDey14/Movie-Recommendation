function getRecommendations() {
    const genre = document.getElementById('genreInput').value.trim();
    const industry = document.getElementById('industrySelect').value;
  
    if (!genre || !industry) {
      alert('Please select industry and enter genre!');
      return;
    }
  
    fetch(`/recommend?genre=${encodeURIComponent(genre)}&industry=${encodeURIComponent(industry)}`)
      .then(response => response.json())
      .then(data => {
        const list = document.getElementById('recommendations');
        list.innerHTML = '';
  
        if (data.length === 0) {
          list.innerHTML = '<li>No movies found!</li>';
        } else {
          data.forEach(movie => {
            const item = document.createElement('li');
            item.textContent = movie.title + " ✨";
            list.appendChild(item);
          });
        }
      })
      .catch(error => {
        console.error('Error fetching recommendations:', error);
      });
  }
  