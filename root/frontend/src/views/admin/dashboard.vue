<template>

    <h2 class="text-center">Admin Dashboard</h2>




    <div>
        <table class="table table-borderless table-light">
            <thead>
                <tr>
                    <th class="text-center fs-3">Students</th>
                    <th class="text-center fs-3">Companies</th>
                    <th class="text-center fs-3">Drives</th>
                    <th class="text-center fs-3">Applications</th>
                </tr>
            </thead>

            <tbody>
                <tr>
                    <td class="text-center fs-1">{{ students }}</td>
                    <td class="text-center fs-1">{{ companies }}</td>
                    <td class="text-center fs-1">{{ drives }}</td>
                    <td class="text-center fs-1">{{ applications }}</td>
                </tr>
            </tbody>
        </table>

        <hr>
        <h2 class="text-center">Manage</h2>

        <table class="table table-borderless table-light">
            <thead>

                <tr>
                    <td class="text-center">
                        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin/students')">
                            Students
                        </button>
                    </td>
                    <td class="text-center">
                        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin/companies')">
                            Companies
                        </button>
                    </td>
                    <td class="text-center">
                        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin/drives')">
                            Drives
                        </button>
                    </td>
                    <td class="text-center">
                        <button class="bg-primary btn shadow text-white" @click="$router.push('/admin/applications')">
                            Applications
                        </button>
                    </td>
                </tr>
            </thead>
        </table>

        <div class="text-center mt-4">
            <button class="bg-danger btn shadow text-white" @click="$router.push('/logout')">Logout</button>
        </div>
    </div>

</template>

<script>

export default {

    data() {

        return {

            students: 0,
            companies: 0,
            drives: 0,
            applications: 0

        }

    },

    async mounted() {

        let token = localStorage.getItem("token")

        let response = await fetch("http://localhost:5000/admin/dashboard", {

            headers: {
                "Authorization": "Bearer " + token
            }

        })

        let data = await response.json()

        if ( data.msg == "Token has expired") {
            alert("Session expired. Please login again.")
            localStorage.removeItem("token")
            this.$router.push("/")
            return
        }

        this.students = data.students
        this.companies = data.companies
        this.drives = data.drives
        this.applications = data.applications

    }

}

</script>