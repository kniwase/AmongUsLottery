<template>
  <b-card
    bg-variant="light"
    title="部屋の設定"
    sub-title="ボタンを押すと警告なしで実行されるため気を付けてください"
  >
    <b-list-group v-if="this.$store.getters.isAdmin">
      <b-list-group-item class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">特殊役の人数を設定する</h5>
        </div>
        <b-container>
          <b-row
            class="mt-2"
            v-for="role in this.$store.getters.roles"
            :key="role.id"
          >
            <b-col>
              <b>{{ role.name }}</b>
            </b-col>
            <b-col>
              <b-form-select
                :options="options[role.id]"
                :value="selected[role.id]"
                @input="onSelectRoleCount($event, role.id)"
                size="sm"
              ></b-form-select>
            </b-col>
          </b-row>
        </b-container>
      </b-list-group-item>
      <b-list-group-item
        class="flex-column align-items-start"
        v-if="this.$store.getters.otherMembers.length"
      >
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">他のユーザーを部屋から追い出す</h5>
        </div>
        <div class="mt-2">
          <b-container class="mt-2">
            <b-row>
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
                  variant="danger"
                  size="sm"
                  v-on:click="onKickUser"
                >
                  追い出す
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </div>
      </b-list-group-item>
      <b-list-group-item class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">他のユーザーの配役を確認する機能の可否</h5>
        </div>
        <div class="mt-2">
          <p>
            現在の設定:
            <b>{{ this.$store.getters.isGodModeAllowed ? "許可" : "拒否" }}</b>
            &nbsp;&nbsp;
            <b-button
              squared
              variant="info"
              size="sm"
              v-on:click="onToggleGodMode"
            >
              切り替える
            </b-button>
          </p>
        </div>
      </b-list-group-item>
      <b-list-group-item class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">この部屋を削除する</h5>
        </div>
        <div class="mt-2">
          <b-button
            squared
            variant="danger"
            size="sm"
            v-on:click="onDeleteRoom"
          >
            削除
          </b-button>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-list-group v-else>
      <b-list-group-item class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">設定は管理者のみが行えます</h5>
        </div>
        <div class="mt-2">
          <b-button
            squared
            variant="danger"
            size="sm"
            v-on:click="onTakeOverAdmin"
            >管理者権限を奪う</b-button
          >
        </div>
      </b-list-group-item>
    </b-list-group>
  </b-card>
</template>

<script>
module.exports = {
  data: () => {
    return {
      updateRoomPropsTimer: null,
      userToBeDeleted: null,
      selected: {},
      options: {},
    };
  },
  methods: {
    range(start, end) {
      return [...Array(end).keys()].slice(start);
    },
    setSelections() {
      this.selected = {};
      this.options = {};
      store.getters.roles.forEach((role) => {
        this.selected[role.id] = role.count;
        this.options[role.id] = this.range(0, 3).map((n) => {
          return { value: n, text: `${n} 人` };
        });
      });
    },
    commitRoomProps(roomProps) {
      store.commit("setRoomProps", roomProps);
      if (store.getters.joined) {
        this.setSelections();
      } else {
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
    onSelectRoleCount(value, id) {
      const roles_new = store.getters.roles.map((role) => {
        return {
          id: role.id,
          name: role.name,
          count: id === role.id ? value : role.count,
        };
      });
      console.log(this.selected);
      console.log(roles_new);
      axios
        .put(`./api/rooms/${store.getters.roomName}/roles`, roles_new)
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