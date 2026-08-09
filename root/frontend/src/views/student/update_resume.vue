<template>

    <h2>Update Resume</h2>

    <form @submit.prevent="updateResume">

        <label>Select Resume</label>
        <input type="file" accept=".pdf" @change="selectResume" required>

        <br><br>

        <button type="submit">Update Resume</button>
        <button type="button" @click="$router.back()">Cancel</button>

    </form>

    <p>{{ message }}</p>


    <div v-if="currentResume" class="text-center">

        <h3>Current Resume</h3>

        <iframe :src="'http://127.0.0.1:5000/static/resumes/' + currentResume" width="700"
            height="990"></iframe>

        <br>
    </div>



</template>

<script>

export default {

    data() {
        return {
            currentResume: "",
            resumeFile: null,
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

            if (response.ok)
                this.currentResume = data.resume
            else
                this.message = data.message
        },

        selectResume(event) {
            this.resumeFile = event.target.files[0]
        },

        async updateResume() {

            let formData = new FormData()

            formData.append("resume", this.resumeFile)

            let response = await fetch(
                "http://127.0.0.1:5000/student/resume/update",
                {
                    method: "PUT",

                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },

                    credentials: "include",

                    body: formData
                }
            )

            let data = await response.json()

            this.message = data.message

            if (response.ok)
                this.getProfile()
        }
    },

    mounted() {
        this.getProfile()
    }

}

</script>