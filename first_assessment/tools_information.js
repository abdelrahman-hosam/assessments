const page = document.getElementsByName('.tool')
const manipulate = document.getElementById('more_details')
const info = [
    ['Insightful tools help you choose your trip dates' , 'If your travel plans are flexible, use the form above to start searching for a specific trip. Then, play around with the Date grid and Price graph options on the Search page to find the cheapest days to get to your destination and back again for round trips.' , './images/1x1-aspect-ratio.png'],
    ['Get smart insights about flight prices' , 'Real-time insights can tell you if a fare is lower or higher than usual, and if the fare you’re seeing is a good price. So, you don’t have to worry about paying too much for a flight or missing out on the cheapest time to book. On some routes, you might also see historical data that helps you better understand how flight prices vary over time.' , './images/1x1-aspect-ratio.png'],
    ['Monitor flight prices and make sure you never miss a price change' , 'Effortlessly track prices for specific travel dates or for any dates, if your plans are flexible, to uncover the best deals. You can easily set up tracking for multiple routes while searching for flights and opt-in to receive email updates when the price changes. Once that.' , './images/1x1-aspect-ratio.png']
]
function show_details(clicked){
    document.querySelectorAll('.tools_info .tool').forEach(tool => tool.classList.remove('active'))
    if(clicked.id === 'tool1'){
        manipulate.querySelector('h3').innerText = info[0][0]
        manipulate.querySelector('p').innerText = info[0][1]
        manipulate.querySelector('img').src = info[0][2]
    }
    else if(clicked.id === 'tool2'){
        manipulate.querySelector('h3').innerText = info[1][0]
        manipulate.querySelector('p').innerText = info[1][1]
        manipulate.querySelector('img').src = info[1][2]
    }
    else{
        manipulate.querySelector('h3').innerText = info[2][0]
        manipulate.querySelector('p').innerText = info[2][1]
        manipulate.querySelector('img').src = info[2][2]
    }
    clicked.classList.add('active')
}
document.addEventListener('DOMContentLoaded', () => {
    const defaultTool = document.getElementById('tool1');
    show_details(defaultTool);
});
