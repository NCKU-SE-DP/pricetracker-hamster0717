<template>
    <nav class="navbar">
        <div class="title">
            <RouterLink to="/overview">價格追蹤小幫手</RouterLink>
            <button @click="openham" >{{opened?'Ｘ':'☰'}}</button>
        </div>
        <ul class="options" v-if="opened">
            <li><RouterLink to="/overview">物價概覽</RouterLink></li>
            <li><RouterLink to="/trending">物價趨勢</RouterLink></li>
            <li><RouterLink to="/news">相關新聞</RouterLink></li>
            <li v-if="!isLoggedIn"><RouterLink to="/login">登入</RouterLink></li>
            <li v-else @click="logout">Hi, {{getUserName}}! 登出</li>
        </ul>
    </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'NavBar',
    data() {
        return {
            opened: true
        }
    },
    computed: {
        isLoggedIn(){
            const userStore = useAuthStore();
            return userStore.isLoggedIn;
        },
        getUserName(){
            const userStore = useAuthStore();
            return userStore.getUserName;
        },
        
    },
    methods: {
        openham(){
            this.opened=!this.opened
        },
        logout(){
            const userStore = useAuthStore();
            userStore.logout();
        }
    }
};
</script>

<style scoped>
.navbar {
    display: flex;
    justify-content: space-between;
    background-color: #f3f3f3;
    padding: 1.5em;
    /*height: 4.5em;*/
    width: 100%;
    align-items: center;
    box-shadow: 0 0 5px #000000;
}
.hamburger{
    font-size: 25px;
    display: none;
}
.navbar ul {
    list-style: none;
    display: flex;
    justify-content: space-around;
}

.title > a{
    font-size: 1.4em;
    font-weight: bold;
    color: #2c3e50 !important;
}

.navbar li {
    color: #575B5D;
    margin: 0 .5em;
    font-size: 1.2em;
}

.navbar li:hover{
    cursor: pointer;
    font-weight: bold;
    background-color:whitesmoke;
}

.navbar a {
    text-decoration: none;
    color: #575B5D;
}
.title > button{
    display: none;
}
@media (max-width: 768px) {
    .navbar li:hover{
        background-color:rgb(176, 198, 198);
        
    }
    .navbar li{
        border-radius: 5px;
        padding: 2px;
    }
    .hamburger{
        font-size: 25px;
        display:contents;
    }
    .title{
        width: 100%;
        padding: 10px 10px 0px 10px;
        display: flex;
        justify-content: space-between;
    }
    .navbar{
        padding: 0;
    }
    .navbar,.navbar ul  {
        flex-direction: column;
    }
    .title > button{
        display: contents;
        font-size: 1.4em;
        font-weight: bold;
        color: #2c3e50 !important;
    }
}
</style>