<template>

    <h2>Students</h2>

    <input type="text" placeholder="Search" v-model="search" @input="getStudents">
    <button @click="clearSearch">Clear</button>

    <br><br>

    <div class="container my-5 shadow p-2 ">
        <div class="table-responsive-md">
            <table class="table table-striped  table-bordered table-hover ">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Course</th>
                        <th>CGPA</th>
                        <th>Graduation Year</th>
                        <th>Skills</th>
                        <th>Blacklist Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    <tr v-if="students.length == 0">
                        <td colspan="10">No students found</td>
                    </tr>

                    <tr v-else v-for="student in students" :key="student.sid">
                        <td>{{ student.sid }}</td>
                        <td>{{ student.name }}</td>
                        <td>{{ student.email }}</td>
                        <td>{{ student.phone }}</td>
                        <td>{{ student.course }}</td>
                        <td>{{ student.cgpa }}</td>
                        <td>{{ student.graduation_year }}</td>
                        <td>{{ student.skills }}</td>
                        <td>{{ student.blacklisted ? "Blocked" : "Not Blocked" }}</td>

                        <td>


                            <button @click="$router.push('/admin/student/' + student.sid)">View Student</button>

                            <button @click="$router.push('/admin/student/' + student.sid + '/applications')">View
                                Applications</button>
                            <button v-if="!student.blacklisted" @click="blacklist(student.sid)">Block</button>
                            <button v-else @click="unblacklist(student.sid)">Unblock</button>
                        </td>
                    </tr>

                </tbody>

            </table>
        </div>
    </div>

</template>

<script>

export default {

    data() {
        return {
            students: [],
            search: ""
        }
    },

    methods: {

        async getStudents() {

            let response = await fetch(
                "http://localhost:5000/admin/students?search=" + this.search,
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.students = await response.json()

            if ( data.msg == "Token has expired") {
                alert("Session expired. Please login again.")
                localStorage.removeItem("token")
                this.$router.push("/")
                return
            }

        },

        clearSearch() {
            this.search = ""
            this.getStudents()
        },

        async blacklist(sid) {

            await fetch(
                "http://localhost:5000/admin/student/" + sid + "/blacklist",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getStudents()

        },

        async unblacklist(sid) {

            await fetch(
                "http://localhost:5000/admin/student/" + sid + "/unblacklist",
                {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            this.getStudents()

        }

    },

    mounted() {
        this.getStudents()
    }

}

</script>