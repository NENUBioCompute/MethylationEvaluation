<template>
  <div class="contact-us">
    <h1>Contact Us</h1>
    <form @submit="submitForm">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="name" placeholder="姓名或单位名称" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" placeholder="xxx@xx.com" required>
      </div>
      <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" v-model="message" placeholder="您的建议/想法" required></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      message: ''
    };
  },
  methods: {
    submitForm(event) {
      event.preventDefault();
      // 这里可以编写发送邮件或保存表单数据的逻辑
      console.log('Form submitted!');
      console.log('Name:', this.name);
      console.log('Email:', this.email);
      console.log('Message:', this.message);
      // 清空表单字段
      this.name = '';
      this.email = '';
      this.message = '';
    }
  }
};
</script>

<style>
.contact-us {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 5px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 235px;
}

button:hover {
  background-color: #0056b3;
}
</style>
