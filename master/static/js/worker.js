// Открытие/скрытие меню с дополнительной информацией
$(document).ready(function() {

$('.toolbar-item__history__svg').click(function(){
  card_item = this.parentElement.parentElement.parentElement.parentElement
  card_item.querySelector('.task-card__more-information__wrapper').classList.toggle('disable')
})

});

//Запуск задачи в работу и открытие дополнительного окна

$(document).ready(function() { 
  
    $('.event-leftside__button-accept').click(function(){   
      start_working(this)      
    })
    $('.more-info__text__accept').click(function(){
      start_working(this)      
    })

});


function start_working(elem) {
  task_id = elem.dataset.itemid
  start_time_from_data = document.querySelectorAll('.task-card-item[data-category="Выполняется"]')  
  if (start_time_from_data.length > 0)  {
    alert('Нельзя запустить несколько задач одновременно. Пожалуйста завершите другие задачи.')
  } else {

      $.ajax({
  
        url: 'start_working/',
        
        type: 'GET',
        
        data: {'id_task': task_id},
    
        headers: {
            "Accept": "network/json",
            "Content-Type": "network/json",        
        },
        
        success: function(data){ 
          location.reload();          
        },
      
        error: function(){  
        alert('Error!');  
        }      
      }); 
    }
}


//Старт пусконаладки

$('.more-info__text__setting-up').click(function(){
  let task = this;    
  let id_task = task.dataset.itemid;  
  
  $.ajax({

    url: 'setting-up/',
    
    type: 'GET',
    
    data: {'id_task': id_task},

    headers: {
        "Accept": "network/json",
        "Content-Type": "network/json",        
    },
    
    success: function(data){
      console.log(data.answer) 
    },
  
    error: function(){  
    alert('Error!');  
    }      
  });  
})


//Действие при измнении количества записей на листе
let start_value = 0
let all_cards = document.querySelectorAll('.task-card-item')

$(document).ready(function() {
  document.querySelector('.quality-position__title').value = 10
  change_block_in_page()
  $('.quality-position__title').change(() => change_block_in_page(true));
  $('.navigation__right').click(() => right_in_page());

});

function change_block_in_page(pos)  {  
  if (pos == true) {
    start_value = 0
  }    
  let value_re = document.querySelector('.quality-position__title').value
  document.querySelector('.all-task-info__range').innerText = `${start_value + 1}-${start_value + 1} из ${all_cards.length}` 
  for (let i = 0; i < all_cards.length; i++) {
    const element = all_cards[i];
    if (i >= Number(value_re) + Number(start_value) || i < start_value) {
      element.classList.add('disable')
    } else {
        if (element.classList.contains('disable')){
          element.classList.remove('disable')
        }
    }
  }  
} 

function right_in_page() {
  let value_res = document.querySelector('.quality-position__title').value
  
  if (Number(start_value) + Number(value_res) < all_cards.length) {    
    start_value = start_value + Number(value_res)
    change_block_in_page(false)
    
  } else {    
    change_block_in_page(true)
  } 
}

// работа таймера

let seconds = 0;
let minutes = 0;
let hours = 0;
let seconds_end = 0;
let minutes_end = 0;
let hours_end = 0;
let interval;
let timer_start
let timer_end
let timer_end_split


$(document).ready(function() {
  
  start_time_from_data = document.querySelectorAll('span[data-datestartfact]:not([data-datestartfact=""])')
  
 
  
  for (let i = 0; i < start_time_from_data.length; i++) {
    
    let now = new Date();
    const element = start_time_from_data[i];
     
    let element_data = element.dataset.datestartfact    
    let norm_date = moment(element_data, 'YYYY-MM-DD h:mm:ss').toDate()
    let sum_time = (now - norm_date)/1000/60/60
    hours = Math.trunc(sum_time)
    let minute_sum =(sum_time - Math.trunc(sum_time)) * 60
    minutes = Math.trunc((sum_time - Math.trunc(sum_time)) * 60)
    seconds = Math.trunc((minute_sum - minutes) * 60)
    timer_start = element.parentElement.querySelectorAll('.task-information__left-side__text')[3]
    timer_end = element.parentElement.querySelectorAll('.task-information__left-side__text')[4]    
    timer_end_split = timer_end.childNodes[1].innerText.split(':')
    seconds_end = Number(timer_end_split[2]);
    minutes_end = Number(timer_end_split[1]);
    hours_end = Number(timer_end_split[0]); 
    interval = setInterval(updateTime, 1000);    
  }
    
});


function updateTime() {  
  seconds++;
  if (seconds === 60) {
    minutes++;
    seconds = 0;
  }
  if (minutes === 60) {
    hours++;
    minutes = 0;
  }
  timer_start.textContent = `Затрачено времени: ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  updateTime_end()
  
}

function updateTime_end() {  
  seconds_end--;
  if (seconds_end === 0) {
    minutes_end--;
    seconds_end = 60;
  }
  if (minutes_end === 0) {
    hours_end--;
    minutes_end = 59;
  }
  timer_end.textContent = `Осталось времени: ${hours_end.toString().padStart(2, '0')}:${minutes_end.toString().padStart(2, '0')}:${seconds_end.toString().padStart(2, '0')}`;
}

//Приостановка, отмена задачи

$(document).ready(function() {
  //Отмена выполнения задания
  $('.event-leftside__button-deny, .more-info__text__deny').click(function(){

    let task = this;    
    let id_task = task.dataset.itemid;
    let deny_popup = document.querySelector('.deny_task_popup')
    deny_popup.classList.toggle('disable')
    deny_popup.querySelector('.pause_task_popup_cansel-button').addEventListener('click', ()=>{deny_popup.classList.add('disable')})
    $.ajax({

      url: 'deny_task/',
      
      type: 'GET',
      
      data: {'id_task': id_task},
  
      headers: {
          "Accept": "network/json",
          "Content-Type": "network/json",        
      },
      
      success: function(data){ 
      },
    
      error: function(){  
      alert('Error!');  
      }      
    });
     
  });

  //Приостановка выполнения задания
  $('.more-info__text__paused, .event-leftside__button-pause').click(function(){

    let task = this;    
    let id_task = task.dataset.itemid;
    let paused_popup = document.querySelector('.pause_task_popup')
    paused_popup.classList.toggle('disable')
    paused_popup.querySelector('.pause_task_popup_cansel-button').addEventListener('click', ()=>{paused_popup.classList.add('disable')})
    $.ajax({

      url: 'pause_task/',
      
      type: 'GET',
      
      data: {'id_task': id_task},
  
      headers: {
          "Accept": "network/json",
          "Content-Type": "network/json",        
      },
      
      success: function(data){         
        // location.reload();
        
      },
    
      error: function(){  
      alert('Error!');  
      }      
    });    
  });
});


// Завершение выпонения задания
$(document).ready(function() {

  $('.event-leftside__button-complete-task, .more-info__text__complete').click(function(){

    let task = this;    
    let id_task = task.dataset.itemid;
    let main_block_task = $(`.task-card-item[data-itemid=${id_task}]`)[0]    
    let plan_profile_amount = main_block_task.querySelector('.right-side__required-quantity__amount').innerText
    let fact_profile_amount = main_block_task.querySelector('.right-side__current-quantity__amount').innerText
    if (Number(plan_profile_amount) != Number(fact_profile_amount)) {
      let isUserReady = confirm("Вы уверены, что хотите завершить задачу? Плановое и фактическое количество профиля не совпадают");
      if (isUserReady) {
        $.ajax({

          url: 'complete_task/',
          
          type: 'GET',
          
          data: {'id_task': id_task},
      
          headers: {
              "Accept": "network/json",
              "Content-Type": "network/json",        
          },
          
          success: function(data){ 
            clearInterval(interval);
            location.reload(); 
             
          },
        
          error: function(){  
          alert('Error!');  
          }      
        });
      }
    } else {
        $.ajax({

        url: 'complete_task/',
        
        type: 'GET',
        
        data: {},
    
        headers: {
            "Accept": "network/json",
            "Content-Type": "network/json",        
        },
        
        success: function(data){ 
          clearInterval(interval);         
          location.reload();  
        },
      
        error: function(){  
        alert('Error!');  
        }      
      });
    }  
  }); 
});


// Передача видео через websocket

$(document).ready(function() {
  let list_task = document.querySelectorAll('.task-card-item[data-category="Выполняется"]')
  for (const elem in list_task) {
    if (Object.prototype.hasOwnProperty.call(list_task, elem)) {
      const task = list_task[elem];
      let task_id = task.dataset.itemid
      videoStream(task_id)
    }
  }
})

function videoStream(task_id){  
  const video = document.getElementById('videoElement');
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');
  const socket = new WebSocket(`ws://localhost:8000/ws/video/${task_id}`);
  const img = document.createElement('img');
  video.after(img); // Добавляем изображение на страницу

  navigator.mediaDevices.getUserMedia({ video: true })
  .then(function(stream) {    
      video.srcObject = stream;
  })
  .catch(function(error) {
      console.error("Ошибка доступа к веб-камере:", error);
  });

  socket.onopen = function() {
      setInterval(() => {
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          const imageData = canvas.toDataURL('image/jpeg', 0.4); //0.4 - качество изображения, изменить при плохом обнаружении
          socket.send(JSON.stringify({ image: imageData.split(',')[1] }));
      }, 250); // Отправка кадра каждые 250 мс
  };

  socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const processedImage = data.processed_image;
    const last_id = data.max_id_profile
    let task_count = document.querySelector('.task-card-item[data-category="Выполняется"]')
    task_count.querySelector('.right-side__current-quantity__amount').innerText = Number(last_id)

    // В элемент img отображаем обработанное изображение
    
    img.src = 'data:image/jpeg;base64,' + processedImage;
    
  };
}

















// let mediaRecorder;
// let recordedChunks = [];
// const video = document.getElementById('video-stream-ai');
// const video_socket = new WebSocket('ws://' + window.location.host + '/ws/video/');

// navigator.mediaDevices.getUserMedia({ video: true })
// .then(stream => {
//     video.srcObject = stream;
//     mediaRecorder = new MediaRecorder(stream);

//     mediaRecorder.ondataavailable = function(event) {
//         if (event.data.size > 0) {
//             recordedChunks.push(event.data);
//         }
//     };

//     mediaRecorder.onstop = function() {
//         const blob = new Blob(recordedChunks, { type: 'video/webm' });
//         const reader = new FileReader();
//         reader.readAsDataURL(blob);
//         reader.onloadend = function() {
//             const base64data = reader.result.split(',')[1];  //Извлекаем только данные
//             sendVideo(base64data);
//           };
//           recordedChunks = [];
//       };
//   });

//   document.getElementById('startButton').onclick = function() {
//       recordedChunks = [];
//       mediaRecorder.start();
//   };

//   document.getElementById('stopButton').onclick = function() {
//       mediaRecorder.stop();
//   };

//   function sendVideo(videoData) {
//     video_socket.send(JSON.stringify({
//           'video': videoData
//       }));
//   }

//   video_socket.onmessage = function(event) {
//       const data = JSON.parse(event.data);
//       console.log(data.status);  // Ответ сервера
//   };

























// $(document).ready(function() {

//   interval_count = setInterval(count_profile, 5000);
// })

// function count_profile()  {
  
//   $.ajax({

//     url: 'count_profile/',
    
//     type: 'GET',
    
//     data: {},

//     headers: {
//         "Accept": "network/json",
//         "Content-Type": "network/json",        
//     },
    
//     success: function(data){ 
//       let task_count = document.querySelector('.task-card-item[data-category="Выполняется"]')
//       let task_count_text = task_count.querySelector('.right-side__current-quantity__amount').innerText
//       let task_count_plan = task_count.querySelector('.right-side__required-quantity__amount').innerText
//       task_count.querySelector('.right-side__current-quantity__amount').innerText = data
      
//       if (Number(task_count_plan) <= Number(task_count_text)) {
//         clearInterval(interval_count);
//         alert('Изготовлено необходимое количество профиля');  
//       }
//     },
  
//     error: function(){  
//     // alert('Error!');
//     clearInterval(interval_count);  
//     }      
//   });  
// }



