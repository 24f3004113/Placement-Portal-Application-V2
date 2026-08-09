<template>

    <h2>Application Details</h2>

    <table border="1" v-if="application">
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
                <td>Application Date</td>
                <td>{{ application.application_date }}</td>
            </tr>
            <tr>
                <td>Status</td>
                <td>{{ application.status }}</td>
            </tr>
            <tr>
                <td>Feedback</td>
                <td>{{ application.feedback }}</td>
            </tr>
        </tbody>

    </table>

    <br>

    <h2>Update Interview</h2>

    <form @submit.prevent="updateInterview">

        <label>Interview Date</label>
        <input type="date" v-model="form.interview_date" required>

        <br><br>

        <label>Interview Time</label>
        <input type="time" v-model="form.interview_time" required>

        <br><br>

        <label>Interview Mode</label>
        <select v-model="form.interview_mode" required>
            <option value="Online">Online</option>
            <option value="Offline">Offline</option>
        </select>

        <br><br>

        <label>Interview Link</label>
        <input type="text" v-model="form.interview_link">

        <br><br>

        <label>Interview Location</label>
        <input type="text" v-model="form.interview_location">

        <br><br>

        <label>Remarks</label>
        <textarea v-model="form.remarks"></textarea>

        <br><br>

        <button type="submit">Update Interview</button>
        <button type="button" @click="$router.back()">Cancel</button>

    </form>

    <p>{{ message }}</p>

</template>

<script>

export default {

    data() {
        return {
            application: null,

            form: {
                iid: "",
                application_id: "",
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

        async getInterview() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/application/" +
                this.$route.params.aid +
                "/interview",
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (response.ok) {

                this.form = {
                    iid: data.iid,
                    application_id: data.application_id,
                    interview_date: data.interview_date,
                    interview_time: data.interview_time,
                    interview_mode: data.interview_mode,
                    interview_link: data.interview_link,
                    interview_location: data.interview_location,
                    remarks: data.remarks
                }

                this.getApplication(data.application_id)

            } else {
                this.message = data.message
            }
        },

        async getApplication(aid) {

            let response = await fetch(
                "http://127.0.0.1:5000/company/application/" + aid,
                {
                    headers: {
                        "Authorization":
                            "Bearer " + localStorage.getItem("token")
                    },
                    credentials: "include"
                }
            )

            let data = await response.json()

            if (response.ok)
                this.application = data
            else
                this.message = data.message

        },

        async updateInterview() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/interview/" +
                this.form.iid +
                "/update",
                {
                    method: "PUT",
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

            this.message = data.message

            if (response.ok)
                this.$router.back()
        }

    },

    mounted() {
        this.getInterview()
    }

}

</script>