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
        joined: state => {
            if (Object.keys(state.room).length !== 0 && state.room.members.length !== 0) {
                return true
            } else {
                return false
            }
        },
        isGodModeAllowed: state => {
            if (Object.keys(state.room).length !== 0 && state.room.members.length !== 0) {
                return state.room.allow_god_mode
            } else {
                return false
            }
        },
        members: state => {
            if (Object.keys(state.room).length !== 0 && state.room.members.length !== 0) {
                return state.room.members
            } else {
                return []
            }
        },
        isAdmin: state => {
            if (Object.keys(state.room).length !== 0 && state.room.members.length !== 0 && state.userName) {
                return state.room.admin === state.userName
            } else {
                return false
            }
        },
        isRoleDecided: state => {
            return Object.keys(state.room).length !== 0 && state.room.role_members.length !== 0;
        },
        roles: state => {
            if (Object.keys(state.room).length !== 0) {
                return state.room.roles;
            } else {
                return [];
            }
        },
        myRole: state => {
            if (Object.keys(state.room).length !== 0 && state.room.role_members.length !== 0 && state.userName) {
                let role_name = "通常役";
                state.room.role_members.forEach(role => {
                    if (role.members.includes(state.userName)) {
                        role_name = role.name;
                    }
                })
                return role_name;
            } else {
                return ""
            }
        },
        lotTimestamp: state => {
            if (Object.keys(state.room).length !== 0) {
                return state.room.lot_timestamp;
            } else {
                return null
            }
        },
        membersTable: state => {
            if (Object.keys(state.room).length !== 0) {
                return state.room.members.map((userName) => {
                    const row = {};
                    row["ユーザー名"] = userName;
                    row["管理者"] = state.room.admin === userName ? "✔" : "";
                    return row;
                });
            } else {
                return []
            }
        },
        membersTableWithRole: state => {
            if (Object.keys(state.room).length !== 0) {
                return state.room.members.map((userName) => {
                    const row = {};
                    row["ユーザー名"] = userName;
                    row["配役"] = "通常役";
                    state.room.role_members.forEach(role => {
                        if (role.members.includes(userName)) {
                            row["配役"] = role.name;
                        }
                    })
                    row["管理者"] = state.room.admin === userName ? "✔" : "";
                    return row;
                });
            } else {
                return []
            }
        },
        otherMembers: state => {
            if (Object.keys(state.room).length !== 0) {
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