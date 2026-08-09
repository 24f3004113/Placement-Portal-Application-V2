<template>

    <h2>Edit Profile</h2>

    <form @submit.prevent="updateProfile">

        <label>Name</label>
        <input type="text" v-model="form.name" required>

        <br><br>

        <label>Email</label>
        <input type="email" v-model="form.email" required>

        <br><br>

        <label>Password</label>
        <input type="password" v-model="form.password">

        <br><br>

        <label>Phone</label>
        <input type="text" v-model="form.phone" required>

        <br><br>

        <label>Course</label>
        <input type="text" v-model="form.course" required>

        <br><br>

        <label>CGPA</label>
        <input type="number" step="0.01" v-model="form.cgpa" required>

        <br><br>

        <label>Graduation Year</label>
        <input type="number" v-model="form.graduation_year" required>

        <br><br>

        <label>Skills</label>
        <textarea v-model="form.skills"></textarea>

        <br><br>

        <button type="submit">Update Profile</button>
        <button type="button" @click="$router.back()">Cancel</button>

    </form>

    <p>{{ message }}</p>

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

        async getProfile() {

            let response = await fetch(
                "http://127.0.0.1:5000/student/profile",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

                        if (response.status == 401 && data.msg == "Token has expired") {

                alert("Session expired. Please login again.")

                localStorage.removeItem("token")

                this.$router.push("/")

                return
            }

            if (response.ok) {

                this.form.name = data.name
                this.form.email = data.email
                this.form.phone = data.phone
                this.form.course = data.course
                this.form.cgpa = data.cgpa
                this.form.graduation_year = data.graduation_year
                this.form.skills = data.skills

            } else {

                this.message = data.message

            }

        },

        async updateProfile() {

            let data = {
                name: this.form.name,
                email: this.form.email,
                phone: this.form.phone,
                course: this.form.course,
                cgpa: this.form.cgpa,
                graduation_year: this.form.graduation_year,
                skills: this.form.skills
            }

            if (this.form.password)
                data.password = this.form.password

            let response = await fetch(
                "http://127.0.0.1:5000/student/profile/update",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },

                    credentials: "include",

                    body: JSON.stringify(data)
                }
            )

            let result = await response.json()


            this.message = result.message

            if (response.ok) {
                alert(result.message)
                this.$router.push("/student")
            } else {
                alert(result.message)
            }

        }

    },

    mounted() {
        this.getProfile()
    }

}

</script>