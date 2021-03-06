const amgusLotData = JSON.parse(localStorage.getItem("amgus-lot-data")) || {
    roomName: null,
    userName: null
};

const store = new Vuex.Store({
    state: {
        roomName: amgusLotData.roomName,
        userName: amgusLotData.userName,
        room: new Object()
    },
    getters: {
        roomName: state => state.roomName,
        userName: state => state.userName,
        isGodModeAllowed: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                return state.room.allow_god_mode
            } else {
                return false
            }
        },
        joined: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                return true
            } else {
                return false
            }
        },
        members: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                return state.room.members
            } else {
                return []
            }
        },
        admin: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                return state.room.admin
            } else {
                return ""
            }
        },
        isAdmin: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                if (state.room.admin && state.userName) {
                    return state.room.admin === state.userName
                } else {
                    return false
                }
            } else {
                return false
            }
        },
        winner: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                return state.room.winner
            } else {
                return ""
            }
        },
        isWinner: state => {
            if (Object.keys(state.room).length && state.room.members.length !== 0) {
                if (state.room.winner && state.userName) {
                    return state.room.winner === state.userName
                } else {
                    return false
                }
            } else {
                return false
            }
        },
        membersTable: state => {
            if (Object.keys(state.room).length) {
                return state.room.members.map((userName) => {
                    const row = {};
                    row["ユーザー名"] = userName;
                    row["管理者"] = state.room.admin === userName ? "👑" : "";
                    return row;
                });
            } else {
                return []
            }
        },
        membersTableWithWinner: state => {
            if (Object.keys(state.room).length) {
                return state.room.members.map((userName) => {
                    const row = {};
                    row["ユーザー名"] = userName;
                    row["管理者"] = state.room.admin === userName ? "👑" : "";
                    row["特殊役"] = state.room.winner === userName ? "😏" : "";
                    return row;
                });
            } else {
                return []
            }
        },
        otherMembers: state => {
            if (Object.keys(state.room).length) {
                return state.room.members.filter(userName => userName !== state.userName);
            } else {
                return []
            }
        },
    },
    mutations: {
        setRoomName(state, roomName) {
            state.roomName = roomName
        },
        setUserName(state, userName) {
            state.userName = userName
        },
        setRoomProps(state, room) {
            if (Object.keys(room).length && room.members.includes(state.userName)) {
                state.room = room
            } else {
                state.room = {}
            }
        }
    }
});

const router = new VueRouter({
    routes: [
        { path: '/', component: httpVueLoader('./pages/home.vue') },
        { path: '/admin', component: httpVueLoader('./pages/admin.vue') },
        { path: '/faq', component: httpVueLoader('./pages/faq.vue') },
        { path: '/agreements', component: httpVueLoader('./pages/agreements.vue') },
    ]
})

const app = new Vue({
    el: "#app",
    store: store,
    router: router
});