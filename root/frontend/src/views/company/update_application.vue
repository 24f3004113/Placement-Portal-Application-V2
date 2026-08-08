<template>

    <h2>Application Details</h2>



    <table border="1" v-if="application">

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
            <td>Current Status</td>
            <td>{{ application.status }}</td>
        </tr>

        <tr>
            <td>Feedback</td>
            <td>{{ application.feedback }}</td>
        </tr>

    </table>



    <hr>

    <h2>Update Application</h2>

    <form @submit.prevent="updateApplication">

        <label>Status</label>

        <select v-model="form.status" @change="checkStatus" required>
            <option value="Applied" disabled>Applied</option>
            <option value="Shortlisted">Shortlist</option>
            <option value="Interview">Interview</option>
            <option value="Selected">Select</option>
            <option value="Rejected">Reject</option>
        </select>

        <br><br>

        <label>Feedback</label>
        <textarea v-model="form.feedback"></textarea>

        <br><br>

        <div v-if="form.status == 'Selected'">

            <label>Joining Date</label>
            <input type="date" v-model="form.joining_date" required>

            <br><br>

        </div>

        <button type="submit">Update Application</button>
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
                status: "",
                feedback: "",
                joining_date: ""
            },

            message: ""
        }
    },

    methods: {

        async getApplication() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/application/" +
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

            if (response.ok) {

                this.application = data

                this.form.status = data.status
                this.form.feedback = data.feedback || ""

            } else {
                this.message = data.message
            }

        },
        checkStatus() {

            if (this.form.status == "Interview") {

                if (this.application.status == "Shortlisted") {
                    this.$router.push(
                        "/company/application/" +
                        this.$route.params.aid +
                        "/interview"
                    )
                } else {

                    alert("First shortlist the student.")

                    this.form.status = this.application.status

                }
            }

        },

        async updateApplication() {

            let response = await fetch(
                "http://127.0.0.1:5000/company/application/" +
                this.$route.params.aid +
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
        this.getApplication()
    }

}

</script>