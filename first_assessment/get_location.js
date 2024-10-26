function getlocation() {
    const def = { 'lat': 30.02, 'long': 31.14 };
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    const lat = position.coords.latitude;
                    const long = position.coords.longitude;
                    resolve({ lat, long });
                },
                () => {
                    resolve(def);
                }
            );
        } else {
            resolve(def);
        }
    });
}
async function getNearestAirport(){
    try{
        var location = await getlocation();
        const request = await fetch(`https://api/v1/flights/getNearByAirports?q={lat:${location.lat}},{lng:${location.long}}`)
        const data = await request.json()
        const near = data.nearby , recent = data.recent , suggested = data.data.presentation.title
        return {
            near,
            recent,
            suggested
        };
    }
    catch (error){
        return console.warn('something went wrong')
    }
}
async function nearCities() {
    console.log('im here')
    const nearest_airport = await getNearestAirport();
    if (nearest_airport && Array.isArray(nearest_airport.near)) {
        const page = document.querySelector('.airports');
        nearest_airport.near.forEach(airport => {
            var child = document.createElement('button');
            child.innerText = airport;
            page.appendChild(child);
        });
    } else {
        console.warn('No nearby airports found');
    }
}
nearCities()