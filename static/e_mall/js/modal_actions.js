document.addEventListener('DOMContentLoaded', function(){

var followersModal=document.getElementById('followersModal');
var followingModal=document.getElementById('followingModal');

var closeFollowers=document.getElementById('closeFollowers');
var closeFollowing=document.getElementById('closeFollowing');

var followersbtn=document.getElementById('showFollowers');
var followingbtn=document.getElementById('showFollowing');

var followersList=document.getElementById('followersList');
var followingList=document.getElementById('followingList');

function followers_following (){
    if(!followersbtn)return; 
    followersbtn.addEventListener('click', function(){
        followersModal.style.display='block';
    });

    followingbtn.addEventListener('click', function(){
        followingModal.style.display='block';
    });

    closeFollowers.addEventListener('click', function(){
        followersModal.style.display='none';
    });

    closeFollowing.addEventListener('click', function(){
        followingModal.style.display='none';
    });

    window.addEventListener('click', function(event){
        if(event.target==followersModal){
            followersModal.style.display='none';
        }
        if(event.target==followingModal){
            followingModal.style.display='none';
        }
    });

}    
followers_following();
    });