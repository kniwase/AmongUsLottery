<template>
  <b-card
    bg-variant="light"
    title="部屋の設定"
    sub-title="ボタンを押すと警告なしで実行されるため気を付けてください"
  >
    <b-list-group v-if="this.isAdmin">
      <b-list-group-item class="flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">特殊役の人数を設定する</h5>
        </div>
        <b-container>
          <b-row class="mt-2" v-for="role in this.roles" :key="role.id">
            <b-col>
              <b>{{ role.name }}</b>
            </b-col>
            <b-col>
              <b-form-select
                :options="options[role.id]"
                :value="selected[role.id]"
                @change="onSelectRoleCount($event, role.id)"
                size="sm"
              ></b-form-select>
            </b-col>
          </b-row>
        </b-container>
      </b-list-group-item>
      <b-list-group-item
        class="flex-column align-items-start"
        v-if="this.otherMembers.length"
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
                  :options="this.otherMembers"
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
            <b>{{ this.isGodModeAllowed ? "許可" : "拒否" }}</b>
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
      userToBeDeleted: null,
      selected: {},
      options: {},
    };
  },
  computed: {
    ...Vuex.mapGetters([
      "roomName",
      "userName",
      "roles",
      "isGodModeAllowed",
      "isAdmin",
      "otherMembers",
    ]),
  },
  methods: {
    range(start, end) {
      return [...Array(end).keys()].slice(start);
    },
    fetchRoomProps(roomName) {
      axios
        .get(`./api/rooms/${roomName}`)
        .then((response) => {
          store.commit("setRoomProps", response.data);
        })
        .catch(() => {
          store.commit("setRoomProps", {});
        });
    },
    setSelections() {
      this.selected = {};
      this.options = {};
      this.roles.forEach((role) => {
        this.selected[role.id] = role.count;
        this.options[role.id] = this.range(0, 3).map((n) => {
          return { value: n, text: `${n} 人` };
        });
      });
    },
    onTakeOverAdmin() {
      axios.put(`./api/rooms/${this.roomName}/admin`, {
        user_name: this.userName,
      });
    },
    onSelectRoleCount(value, id) {
      const roles_new = this.roles.map((role) => {
        return {
          id: role.id,
          name: role.name,
          count: id === role.id ? value : role.count,
        };
      });
      axios.put(`./api/rooms/${this.roomName}/roles`, roles_new);
    },
    onKickUser() {
      if (this.userToBeDeleted) {
        axios.delete(
          `./api/rooms/${this.roomName}/members/${this.userToBeDeleted}`
        );
      }
    },
    onToggleGodMode() {
      axios.put(`./api/rooms/${this.roomName}/godmode`);
    },
    onDeleteRoom() {
      const roomName = this.roomName;
      this.saveNames("", this.userName);
      store.commit("setRoomName", "");
      axios.delete(`./api/rooms/${roomName}`);
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
  watch: {
    roles() {
      this.setSelections();
    },
  },
  mounted() {
    this.setSelections();
    this.fetchRoomProps(this.roomName);
  },
};
</script>

<style scoped></style>