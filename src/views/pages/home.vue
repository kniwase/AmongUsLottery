<template>
  <div v-if="this.joined">
    <b-container class="d-flex justify-content-center">
      <p class="mt-2">
        <b>{{ this.roomName }}</b>
        &nbsp;に&nbsp;
        <b>{{ this.userName }}</b>
        &nbsp;として参加&nbsp;&nbsp;
        <b-button pill variant="outline-danger" size="sm" v-on:click="onExit">
          退出する
        </b-button>
      </p>
    </b-container>
    <b-card bg-variant="light" header="特殊役の設定">
      <b-container>
        <b-row class="mt-2" v-for="role in this.roles" :key="role.id">
          <b-col>
            <b>{{ role.name }}</b>
          </b-col>
          <b-col> {{ role.count }} 人 </b-col>
        </b-row>
      </b-container>
    </b-card>
    <b-card bg-variant="light" header="抽選結果">
      <p>
        <span v-if="this.isRoleDecided">
          あなたは&nbsp;
          <strong>
            {{ this.myRole }}
          </strong>
          &nbsp;です
        </span>
        <span v-else>まだ抽選が行われていません</span>
        <span v-if="this.isAdmin">
          &nbsp;&nbsp;
          <b-button pill variant="primary" size="sm" v-on:click="onDrawLot">
            抽選
          </b-button>
        </span>
      </p>
    </b-card>
    <b-card bg-variant="light" :header="`メンバー（合計: ${membersTable.length} 人）`">
      <div v-if="this.isGodMode && this.isGodModeAllowed">
        <b-table striped hover :items="this.membersTableWithRole" />
      </div>
      <div v-else>
        <b-table striped hover :items="this.membersTable" />
      </div>
    </b-card>
    <b-card bg-variant="light" v-if="this.isGodModeAllowed">
      <p>他のユーザーの配役を確認できます。</p>
      <p>
        現在の状態: <b>{{ this.isGodMode ? "表示" : "非表示" }}</b>
        &nbsp;&nbsp;
        <b-button
          pill
          variant="outline-danger"
          size="sm"
          :pressed.sync="isGodMode"
          >切り替える</b-button
        >
      </p>
    </b-card>
  </div>
  <div v-else>
    <b-card
      bg-variant="light"
      title="エントランス"
      sub-title="部屋名とユーザー名を指定してください"
    >
      <b-form @submit="onSubmit" @reset="onReset">
        <b-form-group
          id="input-group-1"
          label="部屋名:"
          label-for="input-1"
          description="指定された部屋が存在すればその部屋への入室を試みます。存在しなければ新しい部屋を作成します。"
        >
          <b-form-input
            id="input-1"
            v-model="roomNameInput"
            placeholder="部屋名を入力"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-2"
          label="ユーザー名:"
          label-for="input-2"
          description="指定されたユーザー名が上記の存在すれば再入室します。存在しなければ新しいユーザーを作成します。"
        >
          <b-form-input
            id="input-2"
            v-model="userNameInput"
            placeholder="ユーザー名を入力"
            required
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">部屋に入る</b-button>
        <b-button type="reset" variant="outline-danger">
          入力をリセット
        </b-button>
      </b-form>
    </b-card>
  </div>
</template>

<script>
module.exports = {
  data: () => {
    return {
      roomNameInput: "",
      userNameInput: "",
      isGodMode: false,
      updateRoomPropsTimer: null,
    };
  },
  computed: {
    ...Vuex.mapGetters([
      "roomName",
      "userName",
      "joined",
      "members",
      "roles",
      "isRoleDecided",
      "isGodModeAllowed",
      "myRole",
      "isAdmin",
      "membersTable",
      "membersTableWithRole",
    ]),
  },
  methods: {
    storeUserProps(roomName, userName, roomProps) {
      store.commit("setRoomName", roomName);
      store.commit("setUserName", userName);
      store.commit("setRoomProps", roomProps);
      this.saveNames(roomName, userName);
    },
    enterRoom(roomName, userName) {
      axios
        .get(`./api/rooms/${roomName}`)
        .then((response) => {
          // 部屋が存在するので、ユーザーがメンバーに含まれるか確認する
          if (response.data.members.includes(userName)) {
            // メンバーに含まれる場合、受け取った値を保存する
            this.storeUserProps(roomName, userName, response.data);
          } else {
            // メンバーに含まれない場合、メンバーを追加する
            axios
              .post(`./api/rooms/${roomName}/members`, { user_name: userName })
              .then((response) => {
                // 受け取った値を保存する
                this.storeUserProps(roomName, userName, response.data);
              });
          }
        })
        .catch((error) => {
          // 部屋が存在しないので部屋を作成する
          axios
            .post("./api/rooms", { room_name: roomName, user_name: userName })
            .then((response) => {
              this.storeUserProps(roomName, userName, response.data);
            });
        });
    },
    onSubmit(event) {
      event.preventDefault();
      this.enterRoom(this.roomNameInput, this.userNameInput);
    },
    onReset(event) {
      event.preventDefault();
      this.roomNameInput = "";
      this.userNameInput = "";
    },
    onExit() {
      const roomName = this.roomName;
      this.saveNames("", this.userName);
      this.roomNameInput = "";
      store.commit("setRoomName", "");
      axios.delete(`./api/rooms/${roomName}/members/${this.userName}`);
    },
    onDrawLot() {
      axios.put(`./api/rooms/${this.roomName}/lot`);
    },
    saveNames(roomName, userName) {
      localStorage.setItem(
        "amgus-lot-data",
        JSON.stringify({
          roomName: roomName,
          userName: userName,
        })
      );
    },
  },
  mounted() {
    this.roomNameInput = this.roomName;
    this.userNameInput = this.userName;
    if (!this.joined && this.roomName && this.userName) {
      this.enterRoom(this.roomName, this.userName);
    }
  },
};
</script>

<style scoped></style>