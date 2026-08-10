<template>

    <h2>Application Details</h2>

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
                    </tbody>
                </table>

            </div>
        </div>
    </div>

    <hr>




    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-lg-5">

                <h2 class="text-center">Update Application</h2>

                <form @submit.prevent="updateApplication" class="form-control">

                    <div class="mb-3">
                        <label class="form-label">Status</label>
                        <select v-model="form.status" @change="checkStatus" class="form-select" required>
                            <option value="Applied" disabled>Applied</option>
                            <option value="Shortlisted" :disabled="isPreviousStatus('Shortlisted')">
                                Shortlist
                            </option>
                            <option value="Interview" :disabled="isPreviousStatus('Interview')">
                                Interview
                            </option>
                            <option value="Selected" :disabled="isPreviousStatus('Selected')">
                                Select
                            </option>
                            <option value="Rejected" :disabled="isPreviousStatus('Rejected')">
                                Reject
                            </option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Feedback</label>
                        <textarea v-model="form.feedback" class="form-control"></textarea>
                    </div>

                    <div v-if="form.status == 'Selected'" class="mb-3">
                        <label class="form-label">Joining Date</label>
                        <input type="date" v-model="form.joining_date" class="form-control" required>
                    </div>

                    <div class="text-center">
                        <button type="submit" class="bg-success btn shadow text-white me-2">
                            Update Application
                        </button>

                        <button type="button" class="btn btn-secondary" @click="$router.back()">Cancel</button>
                    </div>

                </form>

                <p class="text-center mt-3">{{ message }}</p>

                <div class="text-center mt-3">
                    <button class="btn btn-secondary me-2" @click="$router.back()">Back</button>

                    <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
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
                status: "",
                feedback: "",
                joining_date: ""
            },
            previousStatus: "",

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

            if (data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

            if (response.ok) {

                this.application = data

                this.form.status = data.status
                this.previousStatus = data.status
                this.form.feedback = ""

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


        isPreviousStatus(status) {

            let order = {
                Applied: 1,
                Shortlisted: 2,
                Interview: 3,
                Selected: 4,
                Rejected: 4
            }

            return order[status] <= order[this.previousStatus]
        },

        async updateApplication() {

            let response = await fetch(
                "http://localhost:5000/company/application/" +
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