<template>
  <b-card
    bg-variant="light"
    title="部屋の設定"
    sub-title="ボタンを押すと警告なしで実行されるため気を付けてください"
  >
    <div v-if="this.$store.getters.isAdmin">
      <ul id="settings">
        <li>
          <p>他のユーザーを部屋から追い出す</p>
          <b-container
            class="mt-2"
            v-if="this.$store.getters.otherMembers.length"
          >
            <b-row class="d-flex justify-content-start">
              <b-col>
                <b-form-select
                  v-model="userToBeDeleted"
                  :options="this.$store.getters.otherMembers"
                  size="sm"
                ></b-form-select>
              </b-col>
              <b-col>
                を&nbsp;
                <b-button
                  squared
                  variant="outline-danger"
                  size="sm"
                  v-on:click="onKickUser"
                >
                  追い出す
                </b-button>
              </b-col>
            </b-row>
          </b-container>
          <p v-else>他のユーザーがいないため現在は実行できません</p>
        </li>
        <li class="mt-2">
          <p>神の目（誰が特殊役か確認できる）機能の可否</p>
          <p>
            現在の設定:
            <b>{{ this.$store.getters.isGodModeAllowed ? "許可" : "拒否" }}</b>
            &nbsp;&nbsp;
            <b-button
              squared
              variant="outline-info"
              size="sm"
              v-on:click="onToggleGodMode"
            >
              切り替える
            </b-button>
          </p>
        </li>
        <li class="mt-2">
          <p>
            この部屋を削除する&nbsp;&nbsp;
            <b-button
              squared
              variant="outline-danger"
              size="sm"
              v-on:click="onDeleteRoom"
            >
              削除
            </b-button>
          </p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p class="mt-2">
        設定は管理者のみが行えます&nbsp;&nbsp;
        <b-button
          squared
          variant="danger"
          size="sm"
          v-on:click="onTakeOverAdmin"
          >管理者権限を奪う</b-button
        >
      </p>
    </div>
  </b-card>
</template>

<script>
module.exports = {
  data: () => {
    return {
      updateRoomPropsTimer: null,
      userToBeDeleted: null,
    };
  },
  methods: {
    commitRoomProps(roomProps) {
      store.commit("setRoomProps", roomProps);
      if (!store.getters.joined) {
        router.push("/");
      }
    },
    updateRoomProps() {
      axios
        .get(`./api/rooms/${store.getters.roomName}`)
        .then((response) => {
          this.commitRoomProps(response.data);
        })
        .catch(() => {
          this.clearUpdateRoomPropsTimer();
          this.commitRoomProps({});
        });
    },
    setUpdateRoomPropsTimer() {
      this.updateRoomPropsTimer = setInterval(this.updateRoomProps, 2000);
    },
    clearUpdateRoomPropsTimer() {
      if (this.updateRoomPropsTimer !== null) {
        clearInterval(this.updateRoomPropsTimer);
      }
    },
    onTakeOverAdmin() {
      axios
        .put(`./api/rooms/${store.getters.roomName}/admin`, {
          user_name: store.getters.userName,
        })
        .then((response) => {
          // 受け取った値を保存する
          this.commitRoomProps(response.data);
        });
    },
    onKickUser() {
      if (this.userToBeDeleted) {
        axios
          .delete(
            `./api/rooms/${store.getters.roomName}/members/${this.userToBeDeleted}`
          )
          .then(() => {
            this.commitRoomProps({});
          });
      }
    },
    onToggleGodMode() {
      axios
        .put(`./api/rooms/${store.getters.roomName}/godmode`)
        .then((response) => {
          // 受け取った値を保存する
          this.commitRoomProps(response.data);
        });
    },
    onDeleteRoom() {
      const roomName = store.getters.roomName;
      this.clearUpdateRoomPropsTimer();
      this.saveNames("", store.getters.userName);
      store.commit("setRoomName", "");
      axios.delete(`./api/rooms/${roomName}`).then(() => {
        this.commitRoomProps({});
      });
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
    this.updateRoomProps();
    if (store.getters.joined) {
      this.setUpdateRoomPropsTimer();
    }
  },
  destroyed() {
    this.clearUpdateRoomPropsTimer();
  },
};
</script>

<style scoped></style>