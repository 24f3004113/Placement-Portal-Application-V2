<template>

    <h2>Student Registration</h2>

    <form @submit.prevent="register">

        <label>Name</label>
        <input type="text" v-model="form.name" placeholder="Enter your Name" required><br><br>

        <label>Email</label>
        <input type="email" v-model="form.email" placeholder="Enter your Email" required><br><br>

        <label>Password</label>
        <input type="password" v-model="form.password" placeholder="Create Password" required><br><br>

        <label>Phone Number</label>
        <input type="text" v-model="form.phone" placeholder="Enter your Phone Number" required><br><br>

        <label>Course</label>
        <input type="text" v-model="form.course" placeholder="Enter Studied Course" required><br><br>

        <label>CGPA</label>
        <input type="number" step="0.01" v-model="form.cgpa" placeholder="Enter your CGPA" required><br><br>

        <label>Graduation Year</label>
        <input type="number" v-model="form.graduation_year" placeholder="Enter your Graduation Year" required><br><br>

        <label>Skills</label>
        <input type="text" v-model="form.skills" placeholder="List your Skills"><br><br>

        <button type="submit">Register</button>

    </form>

    <p>{{ message }}</p>

    <button @click="$router.push('/')">Back to Login</button>

</template>

<script>

export default {

    data() {
        return {
            form: {
                name: "",
                email: "",
                password: "",
                phone: "",
                course: "",
                cgpa: "",
                graduation_year: "",
                skills: ""
            },
            message: ""
        }
    },

    methods: {

        async register() {

            let response = await fetch("http://127.0.0.1:5000/student/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.form)
            })

            let data = await response.json()

            this.message = data.message

            if (response.ok) {
                this.$router.push("/")
            }
        }

    }

}

</script>