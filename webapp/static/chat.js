document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
let room='Game'
join_room('Game')


        document.querySelector('.msger-send-btn').onclick=()=>{
        var mes=document.querySelector('#input').value
        document.querySelector('#input').innerHTML=''
        var today=new Date()
        var date="Month "+today.getMonth()+" Day"+today.getDate()+" "+today.getHours()+":"+today.getMinutes()
        msg={'msg':mes,'username':username,'room':room,"date":date}
        socket.emit('input',msg)
//        console.log('jssss')
    }

    socket.on('message',data=>{
    printsys(data)
    })

    socket.on('announce', data =>{
    console.log("in announce")
    show(data)
    })


    document.querySelectorAll('.select-room').forEach(p =>{
    p.onclick=()=>{
        let newRoom=p.innerHTML;
        if(newRoom==room){
        msg=`Already in ${room} Room`
        printsys(msg)
        }
        else{

        leave_room(room)
        join_room(newRoom)
        room =newRoom

        }
    }
    })

        function leave_room(room){
        socket.emit('leave_room',{'username':username,'room':room})
        }

        function join_room(room){
        socket.emit('join_room',{'username':username,'room':room})
        socket.emit('memory',{'room':room})
        document.querySelector('.msger-chat').innerHTML=''
        }

        function printsys(msg){
        const p=document.createElement('alert')
        p.innerHTML=msg
        document.querySelector('.noti').append(p)
        setTimeout(()=>{
        document.querySelector('.noti alert').remove()
        },5000)
        }

        socket.on('cache' , data =>{
//        console.log(data)
            for(let i=0 ;i<data['cache'].length;i++)
            {
                show(data['cache'][i])
            }
        })
        function show(data){
//        console.log("in show")
        if(data.msg)
    {
        if(data.username==username)
        {
//         console.log(data.username)

            let side='right'
            chatbox(side,data)
//            console.log(data)
            }
            else{
            let side='left'
            chatbox(side,data)
            }
            }
        else{printsys(data)}

        }

        function chatbox(side,data){
//            console.log("in chatbox")
            const div=document.createElement('div')
            var ele=document.querySelector(`.msg ${side}-msg`)
            div.innerHTML=`
            <div class="msg ${side}-msg">
            <div
             class="msg-img"

            ></div>

            <div class="msg-bubble">
              <div class="msg-info">
                <div id='clk' class="msg-info-name">${data.username}</div>
                <div class="msg-info-time">${data.room}<br>${data.time}</div>
              </div>

              <div class="msg-text">
                ${data.msg}
              </div>
            </div>
            </div>`
                  document.querySelector('.msger-chat').append(div)
                  document.querySelector('.msger-chat').scrollBy(0,400)
        }


})
