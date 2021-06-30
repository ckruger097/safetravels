const states = [
    { name: 'alaska' },
    { name: 'alabama' },
    { name: 'arkansas' },
    { name: 'arizona' },
    { name: 'california' },
    { name: 'colorado' },
    { name: 'connecticut' },
    { name: 'district of columbia' },
    { name: 'delaware' },
    { name: 'florida' },
    { name: 'georgia' },
    { name: 'hawaii' },
    { name: 'iowa' },
    { name: 'idaho' },
    { name: 'illinois' },
    { name: 'indiana' },
    { name: 'kansas' },
    { name: 'kentucky' },
    { name: 'louisiana' },
    { name: 'massachusetts' },
    { name: 'maryland' },
    { name: 'maine' },
    { name: 'michigan' },
    { name: 'minnesota' },
    { name: 'missouri' },
    { name: 'northern mariana islands' },
    { name: 'mississippi' },
    { name: 'montana' },
    { name: 'north carolina' },
    { name: 'north dakota' },
    { name: 'nebraska' },
    { name: 'new hampshire' },
    { name: 'new jersey' },
    { name: 'new mexico' },
    { name: 'nevada' },
    { name: 'new york' },
    { name: 'ohio' },
    { name: 'oklahoma' },
    { name: 'oregon' },
    { name: 'pennsylvania' },
    { name: 'puerto rico' },
    { name: 'rhode island' },
    { name: 'south carolina' },
    { name: 'south dakota' },
    { name: 'tennessee' },
    { name: 'texas' },
    { name: 'utah' },
    { name: 'virginia' },
    { name: 'vermont' },
    { name: 'washington' },
    { name: 'wisconsin' },
    { name: 'west virginia' },
    { name: 'wyoming' }
];
let search = document.querySelector(".search");
let clear = document.querySelector(".clear");
search.onclick = function(){
    document.querySelector(".container").classList.toggle('active');
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', () => {
        const value = event.target.value;
        console.log(value);
    });
}
clear.onclick = function(){
    document.getElementById("search").value = "";
}