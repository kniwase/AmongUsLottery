<template>
  <div v-if="this.$store.getters.joined">
    <b-container class="d-flex justify-content-center">
      <p class="mt-2">
        <b>{{ this.$store.getters.roomName }}</b>
        &nbsp;に&nbsp;
        <b>{{ this.$store.getters.userName }}</b>
        &nbsp;として参加&nbsp;&nbsp;
        <b-button pill variant="outline-danger" size="sm" v-on:click="onExit"
          >退出する</b-button
        >
      </p>
    </b-container>
    <b-card bg-variant="light" header="特殊役の設定">
      <b-container>
        <b-row
          class="mt-2"
          v-for="role in this.$store.getters.roles"
          :key="role.id"
        >
          <b-col>
            <b>{{ role.name }}</b>
          </b-col>
          <b-col> {{ role.count }} 人 </b-col>
        </b-row>
      </b-container>
    </b-card>
    <b-card bg-variant="light" header="抽選結果">
      <p>
        <span v-if="this.$store.getters.isRoleDecided">
          あなたは&nbsp;
          <strong>
            {{ this.$store.getters.myRole }}
          </strong>
          &nbsp;です
        </span>
        <span v-else>まだ抽選が行われていません</span>
        <span v-if="this.$store.getters.isAdmin">
          &nbsp;&nbsp;
          <b-button pill variant="primary" size="sm" v-on:click="onDrawLot">
            抽選
          </b-button>
        </span>
      </p>
    </b-card>
    <b-card bg-variant="light" header="メンバー">
      <div v-if="this.isGodMode && this.$store.getters.isGodModeAllowed">
        <b-table
          striped
          hover
          :items="this.$store.getters.membersTableWithRole"
        />
      </div>
      <div v-else>
        <b-table striped hover :items="this.$store.getters.membersTable" />
      </div>
    </b-card>
    <b-card bg-variant="light" v-if="this.$store.getters.isGodModeAllowed">
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
            v-model="roomName"
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
            v-model="userName"
            placeholder="ユーザー名を入力"
            required
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">部屋に入る</b-button>
        <b-button type="reset" variant="outline-danger"
          >入力をリセット</b-button
        >
      </b-form>
    </b-card>
  </div>
</template>

<script>
module.exports = {
  data: () => {
    return {
      roomName: store.getters.roomName ? store.getters.roomName : "",
      userName: store.getters.userName ? store.getters.userName : "",
      isGodMode: false,
      updateRoomPropsTimer: null,
    };
  },
  methods: {
    makeToast(message, variant = null) {
      this.$bvToast.toast(message, {
        title: "通知",
        autoHideDelay: 5000,
        variant: variant,
        solid: true,
      });
    },
    commitRoomProps(roomProps) {
      const lotTimestampPrev = store.getters.lotTimestamp;
      const isAdminPrev = store.getters.isAdmin;
      store.commit("setRoomProps", roomProps);
      if (store.getters.joined) {
        if (store.getters.lotTimestamp !== lotTimestampPrev) {
          if (store.getters.lotTimestamp) {
            let variant = "info";
            if (store.getters.myRole !== "通常役") {
              variant = "danger";
            }
            this.makeToast(
              `あなたは ${store.getters.myRole} に選ばれました`,
              variant
            );
          } else {
            this.makeToast("抽選結果がリセットされました", "warning");
          }
        }
        if (!isAdminPrev && store.getters.isAdmin) {
          this.makeToast("管理者になりました", "secondary");
        } else if (isAdminPrev && !store.getters.isAdmin) {
          this.makeToast("管理者権限を奪われました", "secondary");
        }
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
    callbackAfterEntered(roomName, userName, roomProps) {
      store.commit("setRoomName", roomName);
      store.commit("setUserName", userName);
      this.commitRoomProps(roomProps);
      this.saveNames(store.getters.roomName, store.getters.userName);
      this.setUpdateRoomPropsTimer();
    },
    enterRoom(roomName, userName) {
      axios
        .get(`./api/rooms/${roomName}`)
        .then((response) => {
          // 部屋が存在するので、ユーザーがメンバーに含まれるか確認する
          if (response.data.members.includes(userName)) {
            // メンバーに含まれる場合、受け取った値を保存する
            this.callbackAfterEntered(roomName, userName, response.data);
          } else {
            // メンバーに含まれない場合、メンバーを追加する
            axios
              .post(`./api/rooms/${roomName}/members`, { user_name: userName })
              .then((response) => {
                // 受け取った値を保存する
                this.callbackAfterEntered(roomName, userName, response.data);
              });
          }
        })
        .catch((error) => {
          // 部屋が存在しないので部屋を作成する
          axios
            .post("./api/rooms", { room_name: roomName, user_name: userName })
            .then((response) => {
              this.callbackAfterEntered(roomName, userName, response.data);
            });
        });
    },
    onSubmit(event) {
      event.preventDefault();
      this.enterRoom(this.roomName, this.userName);
    },
    onReset(event) {
      event.preventDefault();
      this.roomName = "";
      this.userName = "";
    },
    onExit() {
      const roomName = store.getters.roomName;
      this.clearUpdateRoomPropsTimer();
      this.saveNames("", store.getters.userName);
      this.roomName = "";
      store.commit("setRoomName", "");
      axios
        .delete(`./api/rooms/${roomName}/members/${store.getters.userName}`)
        .then(() => {
          this.commitRoomProps({});
        });
    },
    onDrawLot() {
      axios
        .put(`./api/rooms/${store.getters.roomName}/lot`)
        .then((response) => {
          // 受け取った値を保存する
          this.commitRoomProps(response.data);
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
    this.isGodMode = false;
    if (store.getters.joined) {
      this.updateRoomProps();
      this.setUpdateRoomPropsTimer();
    } else {
      if (store.getters.roomName && store.getters.userName) {
        this.enterRoom(store.getters.roomName, store.getters.userName);
      }
    }
  },
  destroyed() {
    this.clearUpdateRoomPropsTimer();
  },
};
</script>

<style scoped></style>