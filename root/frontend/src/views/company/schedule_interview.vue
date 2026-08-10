<template>

    <h2 class="text-center">Student Profile</h2>

    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <table class="table table-bordered " v-if="application">
        <tbody>
            <tr>
                <td>Student</td>
                <td>{{ application.student }}</td>
            </tr>

            <tr>
                <td>Email</td>
                <td>{{ application.email }}</td>
            </tr>

            <tr>
                <td>Phone</td>
                <td>{{ application.phone }}</td>
            </tr>

            <tr>
                <td>Course</td>
                <td>{{ application.course }}</td>
            </tr>

            <tr>
                <td>CGPA</td>
                <td>{{ application.cgpa }}</td>
            </tr>

            <tr>
                <td>Job Title</td>
                <td>{{ application.job_title }}</td>
            </tr>

            <tr>
                <td>Status</td>
                <td>{{ application.status }}</td>
            </tr>
        </tbody>
    </table>
                </div>
        </div>
    </div>

    <br>

 <div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">

            <h2 class="text-center">Schedule Interview</h2>

            <form @submit.prevent="scheduleInterview" class="form-control">

                <div class="mb-3">
                    <label class="form-label">Interview Date</label>
                    <input type="date" v-model="form.interview_date"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Interview Time</label>
                    <input type="time" v-model="form.interview_time"
                        class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Interview Mode</label>
                    <select v-model="form.interview_mode"
                        class="form-select" required>
                        <option value="">Select Mode</option>
                        <option value="Online">Online</option>
                        <option value="Offline">Offline</option>
                    </select>
                </div>

                <div class="mb-3">
                    <label class="form-label">Interview Link</label>
                    <input type="text" v-model="form.interview_link"
                        class="form-control">
                </div>

                <div class="mb-3">
                    <label class="form-label">Interview Location</label>
                    <input type="text" v-model="form.interview_location"
                        class="form-control">
                </div>

                <div class="mb-3">
                    <label class="form-label">Remarks</label>
                    <textarea v-model="form.remarks"
                        class="form-control"></textarea>
                </div>

                <div class="text-center">
                    <button type="submit"
                        class="bg-success btn shadow text-white me-2">
                        Schedule Interview
                    </button>

                    <button type="button" class="btn btn-secondary"
                        @click="$router.back()">Cancel</button>
                </div>

            </form>

            <p class="text-center mt-3">{{ message }}</p>

            <div class="text-center mt-3">
                <button class="btn btn-secondary me-2"
                    @click="$router.back()">Back</button>

                <button class="bg-danger btn shadow text-white"
                    @click="$router.push('/logout')">Logout</button>
            </div>

        </div>
    </div>
</div>

</template>

<script>

export default {

    data() {
        return {
            application: null,

            form: {
                interview_date: "",
                interview_time: "",
                interview_mode: "",
                interview_link: "",
                interview_location: "",
                remarks: ""
            },

            message: ""
        }
    },

    methods: {

        async getApplication() {

            let response = await fetch(
                "http://localhost:5000/company/application/" +
                this.$route.params.aid,
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            if (response.ok)
                this.application = data
            else
                this.message = data.message

        },

        async scheduleInterview() {

            let response = await fetch(
                "http://localhost:5000/company/application/" +
                this.$route.params.aid +
                "/interview",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include",
                    body: JSON.stringify(this.form)
                }
            )

            let data = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            this.message = data.message

            if (response.ok)
                this.$router.back()

        }

    },

    mounted() {
        this.getApplication()
    }

}

</script>