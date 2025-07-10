import { MigrationInterface, QueryRunner } from "typeorm";

export class DeleteMetabaseVersion1730192147529 implements MigrationInterface {
    name = 'DeleteMetabaseVersion1730192147529'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "product" DROP COLUMN "metabaseVersion"`);
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "UQ_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "client" DROP CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357"`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "UQ_bb082f45ad9dac1c44ac7276357" UNIQUE ("productId")`);
        await queryRunner.query(`ALTER TABLE "product" ADD "metabaseVersion" character varying`);
        await queryRunner.query(`ALTER TABLE "client" ADD CONSTRAINT "FK_bb082f45ad9dac1c44ac7276357" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

}
