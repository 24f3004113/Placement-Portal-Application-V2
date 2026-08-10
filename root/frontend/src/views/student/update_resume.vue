<template>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5">

                <h2 class="text-center">Update Resume</h2>

                <form @submit.prevent="updateResume">

                    <div class="mb-3">
                        <label class="form-label">Select Resume</label>
                        <input type="file" accept=".pdf" @change="selectResume" class="form-control" required>
                    </div>

                    <div class="text-center">
                        <button type="submit" class="bg-success btn shadow text-white me-2">
                            Update Resume
                        </button>

                        <button type="button" class="btn btn-secondary" @click="$router.back()">Cancel</button>
                    </div>

                </form>

                <p class="text-center mt-3">{{ message }}</p>



            </div>
        </div>
    </div>


    <div v-if="currentResume" class="text-center">

        <h3>Current Resume</h3>

        <iframe :src="'http://localhost:5000/static/resumes/' + currentResume" width="700" height="990"></iframe>

        <br>
    </div>


    <div class="text-center mt-3">
        <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>

        <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
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
                "http://localhost:5000/student/profile",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (data.msg == "Token has expired") {

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
                "http://localhost:5000/student/resume/update",
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

            if (data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

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