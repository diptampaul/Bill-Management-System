console.log("javascript Loaded Main")
//answers
//const greetings = ['Hello Mate', 'How are you doing today?', "What's Up homeboi"]


//dom
const btn = document.querySelector('.talk');
const group = document.querySelector('.group')
const group_cls = document.querySelector('.group-close')
const main_content = document.querySelector('.box-1')
const group_content = document.querySelector('.box-2')
const submit_btn = document.querySelector('.submit')





group.addEventListener('click',function(e){
main_content.style.display = 'None';
group_content.style.display = 'block';
})

group_cls.addEventListener('click',function(e){
main_content.style.display = 'block';
group_content.style.display = 'none';
})